import { Component, Input } from '@angular/core';
import { SimilarityService } from '../service/similarity.service';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { ResultsService } from '../service/results.service';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css'],
})
export class ResultsComponent {
  modelNames: any[] = [];
  results: any[] = [];
  private resultsSubscription: Subscription;

  constructor(
    private similarityService: SimilarityService,
    private router: Router,
    private resultsService: ResultsService
  ) {
    this.modelNames = similarityService.modelNames;
    this.resultsSubscription = this.resultsService
      .getResults()
      .subscribe((results) => {
        this.results = results;
      });

    if (!this.results || this.results.length === 0) {
      this.router.navigate(['/']);
    }
  }

  goToHomePage(): void {
    this.router.navigate(['/overview']);
  }

  ngOnDestroy() {
    this.resultsSubscription.unsubscribe();
  }
}
