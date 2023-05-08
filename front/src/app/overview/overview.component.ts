import { Component } from '@angular/core';
import { SimilarityService } from '../service/similarity.service';
import { Router } from '@angular/router';
import { ResultsService } from '../service/results.service';

@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.css'],
})
export class OverviewComponent {
  file: File | null = null;
  results: any[] = [];
  isLoading: boolean = false;
  modelNames: any[] = [];

  constructor(
    private similarityService: SimilarityService,
    private router: Router,
    private resultsService: ResultsService
  ) {
    this.modelNames = similarityService.modelNames;
  }

  onFileSelected(event: Event) {
    const target = event.target as HTMLInputElement;
    const files = target.files;

    if (files && files.length > 0) {
      this.file = files[0];
    }
  }

  onSubmit(): void {
    if (!this.file) {
      return;
    }

    this.isLoading = true;

    this.similarityService.calculateSimilarities(this.file).subscribe(
      (response) => {
        this.results = response;
        this.isLoading = false;
        this.resultsService.setResults(this.results);
        this.router.navigate(['/results']);
      },
      (error) => {
        console.error('Error al calcular las similitudes: ', error);
        this.isLoading = false;
      }
    );
  }
}
