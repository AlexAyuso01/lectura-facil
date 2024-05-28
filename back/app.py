import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
from sentence_transformers import SentenceTransformer, util
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.meteor_score import single_meteor_score
from nltk.tokenize import word_tokenize, sent_tokenize
from rouge_score import rouge_scorer
import pyter
import jiwer
# Se crea una instancia del framework Flask para la aplicación
app = Flask(__name__)
# Se activa CORS para permitir solicitudes de cualquier tipo de origen
CORS(app)

# Modelos de Hugging Face que van a ser usados
model_names = [
    "Maite89/Roberta_finetuning_semantic_similarity_stsb_multi_mt",
    "symanto/sn-xlm-roberta-base-snli-mnli-anli-xnli",
    "hiiamsid/sentence_similarity_spanish_es",
]

# Carga los modelos de HuggingFace y los almacenamos en una lista
models = []
for model_name in model_names:
    model = SentenceTransformer(model_name)
    models.append(model)


# Función que carga datos de un archivo CSV y los devuelve en un DataFrame de Pandas
def load_csv_data(file):
    data = pd.read_csv(file, sep=";", header=None, skiprows=1)
    if len(data.columns) != 3:
        raise ValueError("Invalid CSV file")
    data.columns = ["frase_original", "frase_adaptada", "semanticamente_similares"]
    return data

# Define el endpoint de la API para calcular la similitud semántica
@app.route("/similarity", methods=['POST'])
def get_similarity():
    # Si la solicitud no incluye un archivo, se devuelve un error 400 (Bad Request)
    if 'file' not in request.files:
        return "No file found", 400

    # Carga los datos del archivo CSV recibido en la solicitud
    file = request.files['file']
    try:
        csv_data = load_csv_data(file)
    except ValueError:
        return "Invalid CSV file", 400

    # Itera cada fila de los datos
    similarities = []
    for index, row in csv_data.iterrows():
        # Guarda cada columna en una variable
        original_sentence = row["frase_original"]
        adapted_sentence = row["frase_adaptada"]
        true_label = 1 if row["semanticamente_similares"] == "SI" else 0

        model_results = []
        predictions = []

        # Itera a través de cada modelo
        for model in models:
            # Codifica las frases originales y adaptadas en vectores numéricos
            original_embedding = model.encode(original_sentence, convert_to_tensor=True)
            adapted_embedding = model.encode(adapted_sentence, convert_to_tensor=True)

            # Calcula la similitud coseno entre las dos frases, si es negativa, la convierte en 0
            similarity_score = util.pytorch_cos_sim(original_embedding, adapted_embedding).item()
            similarity_score = max(0, similarity_score)

            # Redondea la puntuación de similitud con 3 decimales, y la añade a la lista de los resultados del modelo
            rounded_similarity_score = round(similarity_score, 3)
            model_results.append(float(rounded_similarity_score))

            # Establece la predicción de si son semánticamente similares o no en función de la puntuación de similitud
            prediction = 1 if similarity_score > 0.8 else 0
            predictions.append(prediction)

        # Añade los resultados de cada modelo a la lista similarities
        similarities.append({
            "frase_original": original_sentence,
            "frase_adaptada": adapted_sentence,
            "similitudes": model_results,
            "predicciones": predictions,
            "etiqueta_real": true_label
        })

    # Devuelve los resultados en formato JSON
    return jsonify(similarities)

nltk.download('punkt')
nltk.download('wordnet')

def calculate_wer(reference, hypothesis):
    # Tokeniza el texto en palabras y luego reconvierte a string separado por espacios
    reference_tokens = word_tokenize(reference)
    hypothesis_tokens = word_tokenize(hypothesis)
    
    # Convierte las listas de tokens de vuelta a strings
    reference_str = ' '.join(reference_tokens)
    hypothesis_str = ' '.join(hypothesis_tokens)

    # Calcula el WER con los strings reconstruidos
    return jiwer.wer(reference_str, hypothesis_str)

def calculate_metrics(original, adapted):
    # Tokenización de oraciones y palabras
    original_tokens = word_tokenize(original)
    adapted_tokens = word_tokenize(adapted)
    
    # BLEU score
    smoothie = SmoothingFunction().method4
    bleu_score = sentence_bleu([original_tokens], adapted_tokens, smoothing_function=smoothie)
    
    # ROUGE score
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    rouge_scores = scorer.score(original, adapted)
    rouge_score = {key: rouge_scores[key].fmeasure for key in rouge_scores}
    
    # METEOR score
    meteor_score = single_meteor_score(original_tokens, adapted_tokens)
    
    # TER score (Translation Edit Rate)
    ter_score = pyter.ter(original_tokens, adapted_tokens)
    
    # WER score (Word Error Rate)
    # Asegúrate de pasar las listas de tokens, no las frases completas
    wer_score = calculate_wer(original, adapted)

    return {
        "BLEU": bleu_score,
        "ROUGE-1": rouge_score['rouge1'],
        "ROUGE-L": rouge_score['rougeL'],
        "METEOR": meteor_score,
        "TER": ter_score,
        "WER": wer_score
    }

weights = {
    "BLEU": 1,
    "METEOR": 3,
    "ROUGE-1": 3,
    "ROUGE-L": 3,
    "TER": 2,
    "WER": 2
}

# Define el endpoint de la API para calcular la similitud semántica
@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        try:
            df = pd.read_csv(file, sep=";")
            results = []
            for index, row in df.iterrows():
                original = row['frase_original']
                adapted = row['frase_adaptada']
                metrics = calculate_metrics(original, adapted)  
                quality_indicator = evaluate_quality(metrics, weights)

                individual_qualities = {}
                for metric_name, metric_value in metrics.items():
                    individual_qualities[metric_name] = evaluate_individual_quality(metric_value, metric_name)

                results.append({
                    "original": original,
                    "adapted": adapted,
                    "metrics": metrics,
                    "overall_quality": quality_indicator,  # Calidad general ponderada
                    "individual_qualities": individual_qualities  # Calidades individuales con ponderación
                })
            return jsonify(results)
        except Exception as e:
            return jsonify({"error": str(e)}), 500



def evaluate_quality(metrics, weights):
    thresholds = {
        "high": {
            "BLEU": 0.5,
            "ROUGE-1": 0.6,
            "ROUGE-L": 0.6,
            "METEOR": 0.5,
            "TER": 0.4,
            "WER": 0.3
        },
        "medium": {
            "BLEU": 0.3,
            "ROUGE-1": 0.35,
            "ROUGE-L": 0.35,
            "METEOR": 0.25,
            "TER": 0.5,
            "WER": 0.4
        }
    }

    score_totals = {
        "high": 0,
        "medium": 0,
        "low": 0
    }

    total_weight = sum(weights.values())

    # Calcula el score ponderado
    weighted_scores = {"high": 0, "medium": 0, "low": 0}
    for metric, value in metrics.items():
        category = "low"
        if (metric in ["TER", "WER"] and value <= thresholds["high"][metric]) or (metric not in ["TER", "WER"] and value >= thresholds["high"][metric]):
            category = "high"
        elif (metric in ["TER", "WER"] and value <= thresholds["medium"][metric]) or (metric not in ["TER", "WER"] and value >= thresholds["medium"][metric]):
            category = "medium"
        
        score_totals[category] += weights[metric]
        weighted_scores[category] += weights[metric] * (1 if category == "high" else 0.5 if category == "medium" else 0.25)

    # Calcula el promedio ponderado basado en la categoría
    weighted_average = (weighted_scores["high"] + weighted_scores["medium"] + weighted_scores["low"]) / total_weight

    # Definir los umbrales para la calidad basada en el promedio ponderado
    if weighted_average > 0.75:
        return "high"
    elif weighted_average > 0.5:
        return "medium"
    else:
        return "low"

    
def evaluate_individual_quality(metric_value, metric_name):
    thresholds = {
        "high": {
            "BLEU": 0.5,
            "ROUGE-1": 0.6,
            "ROUGE-L": 0.6,
            "METEOR": 0.5,
            "TER": 0.4,  # Nota: Para TER, más bajo es mejor, así que este es un umbral máximo
            "WER": 0.3   # Nota: Para WER, más bajo es mejor, así que este es un umbral máximo
        },
        "medium": {
            "BLEU": 0.3,
            "ROUGE-1": 0.35,
            "ROUGE-L": 0.35,
            "METEOR": 0.25,
            "TER": 0.5,
            "WER": 0.4
        }
    }
        
    if metric_name in ["TER", "WER"]:  # Para métricas donde menor es mejor
        if metric_value <= thresholds["high"][metric_name]:
            return "high"
        elif metric_value <= thresholds["medium"][metric_name]:
            return "medium"
        else:
            return "low"
    else:  # Para métricas donde mayor es mejor
        if metric_value >= thresholds["high"][metric_name]:
            return "high"
        elif metric_value >= thresholds["medium"][metric_name]:
            return "medium"
        else:
            return "low"

