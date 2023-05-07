import re
import pandas as pd
from flask import Flask, jsonify, request
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
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
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    similarity_pipeline = pipeline("text-classification", model=model, tokenizer=tokenizer)
    models.append(similarity_pipeline)

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

        model_results = []
        for model in models:
            result = model([{"text": original_sentence, "text_pair": adapted_sentence}])
            similarity_score = float(re.findall(r'\d+\.?\d*', result[0]["label"])[0])
            model_results.append(float(similarity_score))

        similarities.append({
            "frase_original": original_sentence,
            "frase_adaptada": adapted_sentence,
            "similitudes": model_results
        })

    return jsonify(similarities)

if __name__ == "__main__":
    app.run()
