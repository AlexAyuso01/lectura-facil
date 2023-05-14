import math

import pandas as pd
from flask import Flask, jsonify, request
from sentence_transformers import SentenceTransformer, util
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Carga los modelos de Hugging Face
model_names = [
    "Maite89/Roberta_finetuning_semantic_similarity_stsb_multi_mt",
    "symanto/sn-xlm-roberta-base-snli-mnli-anli-xnli",
    "hiiamsid/sentence_similarity_spanish_es",
]

models = []
for model_name in model_names:
    model = SentenceTransformer(model_name)
    models.append(model)

def load_csv_data(file_path):
    data = pd.read_csv(file_path, sep=";", header=None, skiprows=1)
    data.columns = ["tipo_frase_original", "frase_original", "frase_adaptada", "semanticamente_similares"]
    return data


@app.route("/similarity", methods=['POST'])
def get_similarity():
    if 'file' not in request.files:
        return "No file found", 400

    file = request.files['file']
    csv_data = load_csv_data(file)

    similarities = []
    for index, row in csv_data.iterrows():
        original_sentence = row["frase_original"]
        adapted_sentence = row["frase_adaptada"]
        true_label = 1 if row["semanticamente_similares"] == "SI" else 0

        model_results = []
        predictions = []
        for model in models:
            original_embedding = model.encode(original_sentence, convert_to_tensor=True)
            adapted_embedding = model.encode(adapted_sentence, convert_to_tensor=True)
            similarity_score = util.pytorch_cos_sim(original_embedding, adapted_embedding).item()
            similarity_score = max(0, similarity_score)

            rounded_similarity_score = round(similarity_score, 3)
            model_results.append(float(rounded_similarity_score))
            prediction = 1 if similarity_score > 0.5 else 0
            predictions.append(prediction)

        similarities.append({
            "frase_original": original_sentence,
            "frase_adaptada": adapted_sentence,
            "similitudes": model_results,
            "predicciones": predictions,
            "etiqueta_real": true_label
        })

    return jsonify(similarities)


if __name__ == "__main__":
    app.run()

