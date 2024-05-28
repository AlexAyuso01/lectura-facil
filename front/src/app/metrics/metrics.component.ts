import { Component, OnInit } from '@angular/core';
import { ResultsService } from '../service/results.service';
import { Router } from '@angular/router';

interface Metric {
  original: string;
  adapted: string;
  metrics: Record<string, number>;
  overall_quality: string;
  individual_qualities: Record<string, string>;
}

@Component({
  selector: 'app-metrics',
  templateUrl: './metrics.component.html',
  styleUrls: ['./metrics.component.css']
})
export class MetricsComponent implements OnInit {
  metrics: Metric[] = [];

  getColor(quality: string): string {
    switch (quality) {
      case 'high':
        return 'green';
      case 'medium':
        return 'orange';
      default:
        return 'red';
    }
  }

  getIndividualColor(individualQuality: string): string {
    switch (individualQuality) {
      case 'high':
        return 'green';
      case 'medium':
        return 'orange';
      default:
        return 'red';
    }
  }

  constructor(
    private resultsService: ResultsService,
    private router: Router) { }

  goToHomePage(): void {
    this.router.navigate(['/overview']);
  }

  ngOnInit(): void {
    this.resultsService.getResults().subscribe(metrics => {
      this.metrics = metrics;
    });
  }
}




