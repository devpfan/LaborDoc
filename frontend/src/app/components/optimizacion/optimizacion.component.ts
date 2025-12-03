import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';
import { ResultadoOptimizacion, Estadisticas } from '../../models/docente.model';

@Component({
  selector: 'app-optimizacion',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './optimizacion.component.html',
  styleUrls: ['./optimizacion.component.scss']
})
export class OptimizacionComponent implements OnInit {
  resultado: ResultadoOptimizacion | null = null;
  necesidades: any = null;
  estadisticas: Estadisticas | null = null;
  cargando = false;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.cargarNecesidades();
    this.cargarEstadisticas();
  }

  cargarNecesidades(): void {
    this.apiService.getNecesidades().subscribe({
      next: (data: any) => {
        this.necesidades = data;
      },
      error: (error: any) => {
        console.error('Error al cargar necesidades:', error);
      }
    });
  }

  cargarEstadisticas(): void {
    this.apiService.getEstadisticas().subscribe({
      next: (data) => {
        this.estadisticas = data;
      },
      error: (error: any) => {
        console.error('Error al cargar estadísticas:', error);
      }
    });
  }

  ejecutarOptimizacion(): void {
    this.cargando = true;
    this.apiService.ejecutarOptimizacion().subscribe({
      next: (data) => {
        this.resultado = data;
        this.cargando = false;
        this.cargarEstadisticas();
      },
      error: (error: any) => {
        console.error('Error al ejecutar optimización:', error);
        this.cargando = false;
        alert('Error al ejecutar la optimización');
      }
    });
  }

  limpiarAsignaciones(): void {
    if (confirm('¿Está seguro de limpiar todas las asignaciones?')) {
      this.apiService.limpiarAsignaciones().subscribe({
        next: () => {
          this.resultado = null;
          this.cargarEstadisticas();
          alert('Asignaciones limpiadas correctamente');
        },
        error: (error: any) => {
          console.error('Error al limpiar asignaciones:', error);
        }
      });
    }
  }

  getDocenteKeys(): string[] {
    return this.resultado?.distribucion_por_docente 
      ? Object.keys(this.resultado.distribucion_por_docente) 
      : [];
  }

  getDocenteInfo(key: string): any {
    return this.resultado?.distribucion_por_docente[key];
  }
}
