import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { Estadisticas } from '../../models/docente.model';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  estadisticas: Estadisticas | null = null;
  necesidades: any = null;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.cargarDatos();
  }

  cargarDatos(): void {
    this.apiService.getEstadisticas().subscribe({
      next: (data) => {
        this.estadisticas = data;
      },
      error: (error: any) => {
        console.error('Error al cargar estadísticas:', error);
      }
    });

    this.apiService.getNecesidades().subscribe({
      next: (data: any) => {
        this.necesidades = data;
      },
      error: (error: any) => {
        console.error('Error al cargar necesidades:', error);
      }
    });
  }
}
