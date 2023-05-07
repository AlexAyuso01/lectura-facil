import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SimilarityService {
  private apiUrl = 'http://127.0.0.1:5000/similarity';

  constructor(private http: HttpClient) {}

  calculateSimilarities(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file, file.name);

    return this.http.post(this.apiUrl, formData);
  }
}
