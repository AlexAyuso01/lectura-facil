import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class ResultsService {
  private resultsSource = new BehaviorSubject<any>(null);
  results$ = this.resultsSource.asObservable();
  private backendUrl = 'http://localhost:5000'; 

  constructor(private http: HttpClient) {}

  setResults(results: any) {
    console.log('Setting results:', results);
    this.resultsSource.next(results);
  }

  getResults() {
    return this.results$;
  }

  calculateMetrics(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`${this.backendUrl}/upload`, formData);
  }
}
