import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ResultsService {
  private resultsSource = new BehaviorSubject<any>(null);
  results$ = this.resultsSource.asObservable();

  setResults(results: any) {
    console.log('Setting results:', results)
    this.resultsSource.next(results);
  }

  getResults() {
    return this.results$;
  }
}
