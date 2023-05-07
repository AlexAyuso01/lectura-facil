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
  isLoading: boolean = false;
  modelNames = [
    "Maite89/Roberta_finetuning_semantic_similarity_stsb_multi_mt",
    "symanto/sn-xlm-roberta-base-snli-mnli-anli-xnli",
    "hiiamsid/sentence_similarity_spanish_es",
  ];  

  constructor(private similarityService: SimilarityService) {}

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
      },
      (error) => {
        console.error("Error al calcular las similitudes: ", error);
        this.isLoading = false;
      }
    );
  }  
}
