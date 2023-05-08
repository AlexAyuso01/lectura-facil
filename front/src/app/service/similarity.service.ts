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
}
