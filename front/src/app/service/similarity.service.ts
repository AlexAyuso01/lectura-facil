import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SimilarityService {
  private apiUrl = 'http://127.0.0.1:5000/similarity';
  modelNames = [
    'Maite89/Roberta_finetuning_semantic_similarity_stsb_multi_mt',
    'symanto/sn-xlm-roberta-base-snli-mnli-anli-xnli',
    'hiiamsid/sentence_similarity_spanish_es',
  ];

  constructor(private http: HttpClient) {}

  calculateSimilarities(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file, file.name);

    return this.http.post(this.apiUrl, formData);
  }

  calculateMetrics(results: any[]): any[] {
    let totalPredictions = results.length;
    let correctPredictions = Array(this.modelNames.length).fill(0);
    let truePositives = Array(this.modelNames.length).fill(0);
    let trueNegatives = Array(this.modelNames.length).fill(0);
    let falsePositives = Array(this.modelNames.length).fill(0);
    let falseNegatives = Array(this.modelNames.length).fill(0);

    for (let i = 0; i < totalPredictions; i++) {
      let trueLabel = results[i]['etiqueta_real'];
      let predictions = results[i]['predicciones'];
      for (let j = 0; j < predictions.length; j++) {
        if (predictions[j] == trueLabel) {
          correctPredictions[j]++;
          if (trueLabel == 1) {
            truePositives[j]++;
          } else {
            trueNegatives[j]++;
          }
        } else {
          if (predictions[j] == 1) {
            falsePositives[j]++;
          } else {
            falseNegatives[j]++;
          }
        }
      }
    }

    let metrics = [];
    for (let j = 0; j < this.modelNames.length; j++) {
      let accuracy = correctPredictions[j] / totalPredictions;
      let precision =
        truePositives[j] + falsePositives[j] > 0
          ? truePositives[j] / (truePositives[j] + falsePositives[j])
          : 0;
      let recall =
        truePositives[j] + falseNegatives[j] > 0
          ? truePositives[j] / (truePositives[j] + falseNegatives[j])
          : 0;
      let f1Score =
        precision + recall > 0
          ? (2 * (precision * recall)) / (precision + recall)
          : 0;
      metrics.push({
        accuracy: accuracy,
        precision: precision,
        recall: recall,
        f1Score: f1Score,
      });
    }

    return metrics;
  }
}
