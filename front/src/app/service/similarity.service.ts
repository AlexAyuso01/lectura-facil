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

  calculateAccuracy(results: any[]): number[] {
    let totalPredictions = results.length;
    let correctPredictions = Array(this.modelNames.length).fill(0);
  
    for (let i = 0; i < totalPredictions; i++) {
      let trueLabel = results[i]["etiqueta_real"];
      let predictions = results[i]["predicciones"];
      for (let j = 0; j < predictions.length; j++) {
        if (predictions[j] == trueLabel) {
          correctPredictions[j]++;
        }
      }
    }
  
    let accuracies = correctPredictions.map(x => x / totalPredictions);
    
    return accuracies;
  }
  
}
