import { Component } from '@angular/core';
import { SimilarityService } from '../service/similarity.service';
import { Router } from '@angular/router';
import { ResultsService } from '../service/results.service';
import { ToastrService } from 'ngx-toastr';
import { CustomToasterComponent } from '../custom-toaster/custom-toaster.component';

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
    private resultsService: ResultsService,
    private toastr: ToastrService
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
        console.log('Redirecting to /results');
        this.router.navigate(['/results']);
        console.log(response);
      },
      (error) => {
        console.error('Error al calcular las similitudes: ', error);
        this.isLoading = false;
        this.toastr.error(
          'Se produjo un error al calcular las similitudes: el formato del CSV no es correcto',
          'Error',
          {
            toastComponent: CustomToasterComponent,
            timeOut: 10000
          }
        );
      }
    );
  }

  onCalculateMetrics(): void {
    if (this.file) {
      this.isLoading = true;
      this.resultsService.calculateMetrics(this.file).subscribe({
        next: (response: any) => {
          this.resultsService.setResults(response);
          this.isLoading = false;
          this.router.navigate(['/metrics']);  
        },
        error: (error: any) => {
          console.error('Error al calcular las métricas:', error);
          this.isLoading = false;
        }
      });
    } else {
      alert('Por favor, selecciona un archivo CSV primero.');
    }
  }  
}
