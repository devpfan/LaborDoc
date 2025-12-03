import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { ConfiguracionColegio } from '../../models/docente.model';

@Component({
  selector: 'app-configuracion',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './configuracion.component.html',
  styleUrls: ['./configuracion.component.scss']
})
export class ConfiguracionComponent implements OnInit {
  configuracion: ConfiguracionColegio | null = null;
  configuracionEditable: ConfiguracionColegio | null = null;
  modoEdicion = false;
  validacion: any = null;
  guardando = false;
  
  grados = [
    'Preescolar', 'Primero', 'Segundo', 'Tercero', 'Cuarto', 
    'Quinto', 'Sexto', 'Séptimo', 'Octavo', 'Noveno', 
    'Décimo', 'Undécimo'
  ];

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.cargarConfiguracion();
  }

  cargarConfiguracion(): void {
    this.apiService.getConfiguracion().subscribe({
      next: (data) => {
        this.configuracion = data;
        this.validarConfiguracion();
      },
      error: (error) => {
        console.error('Error al cargar configuración:', error);
      }
    });
  }

  validarConfiguracion(): void {
    this.apiService.validarConfiguracion().subscribe({
      next: (data) => {
        this.validacion = data;
      },
      error: (error) => {
        console.error('Error al validar configuración:', error);
      }
    });
  }

  iniciarEdicion(): void {
    this.configuracionEditable = JSON.parse(JSON.stringify(this.configuracion));
    this.modoEdicion = true;
  }

  cancelarEdicion(): void {
    this.configuracionEditable = null;
    this.modoEdicion = false;
  }

  guardarConfiguracion(): void {
    if (!this.configuracionEditable) return;

    this.guardando = true;
    this.apiService.updateConfiguracion(this.configuracionEditable).subscribe({
      next: (data) => {
        this.configuracion = data;
        this.modoEdicion = false;
        this.configuracionEditable = null;
        this.guardando = false;
        this.validarConfiguracion();
        alert('Configuración actualizada correctamente.\nLas asignaciones se han limpiado.');
      },
      error: (error) => {
        console.error('Error al guardar configuración:', error);
        this.guardando = false;
        alert('Error al guardar la configuración');
      }
    });
  }

  resetearConfiguracion(): void {
    if (!confirm('¿Está seguro de resetear la configuración a los valores por defecto?\nEsto limpiará todas las asignaciones.')) {
      return;
    }

    this.apiService.resetearConfiguracion().subscribe({
      next: (data) => {
        this.configuracion = data;
        this.modoEdicion = false;
        this.configuracionEditable = null;
        this.validarConfiguracion();
        alert('Configuración reseteada a valores por defecto');
      },
      error: (error) => {
        console.error('Error al resetear configuración:', error);
      }
    });
  }

  getGruposPorGrado(grado: string): number {
    if (this.modoEdicion && this.configuracionEditable) {
      return this.configuracionEditable.grupos_por_grado[grado] || 0;
    }
    return this.configuracion?.grupos_por_grado[grado] || 0;
  }

  setGruposPorGrado(grado: string, valor: number): void {
    if (this.configuracionEditable) {
      this.configuracionEditable.grupos_por_grado[grado] = Math.max(0, valor);
    }
  }

  esGradoSinNiveles(grado: string): boolean {
    return ['Preescolar', 'Primero', 'Segundo', 'Tercero'].includes(grado);
  }

  getTotalGrupos(): number {
    const config = this.modoEdicion ? this.configuracionEditable : this.configuracion;
    if (!config) return 0;
    return Object.values(config.grupos_por_grado).reduce((sum: number, val) => sum + ((val as number) || 0), 0);
  }
}
