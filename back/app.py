import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
from sentence_transformers import SentenceTransformer, util

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


if __name__ == "__main__":
    app.run()
