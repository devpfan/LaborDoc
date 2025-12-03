import { Routes } from '@angular/router';
import { DocentesComponent } from './components/docentes/docentes.component';
import { OptimizacionComponent } from './components/optimizacion/optimizacion.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { ConfiguracionComponent } from './components/configuracion/configuracion.component';

export const routes: Routes = [
  { path: '', component: DashboardComponent },
  { path: 'docentes', component: DocentesComponent },
  { path: 'optimizacion', component: OptimizacionComponent },
  { path: 'configuracion', component: ConfiguracionComponent },
  { path: '**', redirectTo: '' }
];
