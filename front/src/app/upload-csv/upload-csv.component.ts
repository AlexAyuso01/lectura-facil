import { Component } from '@angular/core';
import { SimilarityService } from '../similarity.service';

@Component({
  selector: 'app-upload-csv',
  templateUrl: './upload-csv.component.html',
  styleUrls: ['./upload-csv.component.css'],
})
export class UploadCsvComponent {
  file: File | null = null;
  results: any[] = [];

  constructor(private similarityService: SimilarityService) {}

  onFileSelected(event: Event) {
    const target = event.target as HTMLInputElement;
    const files = target.files;

    if (files && files.length > 0) {
      this.file = files[0];
    }
  }

  onSubmit() {
    if (this.file) {
      this.similarityService.calculateSimilarities(this.file).subscribe(
        (response) => {
          this.results = response;
        },
        (error) => {
          console.error('Error al calcular las similitudes:', error);
        }
      );
    }
  }
}
