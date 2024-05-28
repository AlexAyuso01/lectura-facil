import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { OverviewComponent } from './overview/overview.component';
import { ResultsComponent } from './results/results.component';
import { MetricsComponent } from './metrics/metrics.component'; // Import the MetricsComponent class

const routes: Routes = [
  { path: '', redirectTo: '/overview', pathMatch: 'full' },
  { path: 'overview', component: OverviewComponent },
  { path: 'results', component: ResultsComponent },
  { path: 'metrics', component: MetricsComponent }  // Nueva ruta para mostrar métricas
]; 

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
