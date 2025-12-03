import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { Docente, TipoDocente } from '../../models/docente.model';

@Component({
  selector: 'app-docentes',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './docentes.component.html',
  styleUrls: ['./docentes.component.scss']
})
export class DocentesComponent implements OnInit {
  docentes: Docente[] = [];
  docenteSeleccionado: Docente | null = null;
  modoEdicion = false;
  nuevoDocente: Docente = this.inicializarDocente();
  TipoDocente = TipoDocente;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.cargarDocentes();
  }

  cargarDocentes(): void {
    this.apiService.getDocentes().subscribe({
      next: (data) => {
        this.docentes = data;
      },
      error: (error) => {
        console.error('Error al cargar docentes:', error);
      }
    });
  }

  inicializarDocente(): Docente {
    return {
      nombre: '',
      tipo: TipoDocente.PRIMARIA,
      horas_asignadas: 0,
      grados_asignados: [],
      disponible: true
    };
  }

  seleccionarDocente(docente: Docente): void {
    this.docenteSeleccionado = { ...docente };
    this.modoEdicion = true;
  }

  crearDocente(): void {
    this.apiService.createDocente(this.nuevoDocente).subscribe({
      next: () => {
        this.cargarDocentes();
        this.nuevoDocente = this.inicializarDocente();
      },
      error: (error) => {
        console.error('Error al crear docente:', error);
      }
    });
  }

  actualizarDocente(): void {
    if (this.docenteSeleccionado && this.docenteSeleccionado.id) {
      this.apiService.updateDocente(this.docenteSeleccionado.id, this.docenteSeleccionado).subscribe({
        next: () => {
          this.cargarDocentes();
          this.cancelarEdicion();
        },
        error: (error) => {
          console.error('Error al actualizar docente:', error);
        }
      });
    }
  }

  eliminarDocente(id: number | undefined): void {
    if (id && confirm('¿Está seguro de eliminar este docente?')) {
      this.apiService.deleteDocente(id).subscribe({
        next: () => {
          this.cargarDocentes();
        },
        error: (error) => {
          console.error('Error al eliminar docente:', error);
        }
      });
    }
  }

  cancelarEdicion(): void {
    this.docenteSeleccionado = null;
    this.modoEdicion = false;
  }

  verAsignaciones(id: number | undefined): void {
    if (id) {
      this.apiService.getAsignacionesDocente(id).subscribe({
        next: (data) => {
          console.log('Asignaciones:', data);
          alert(`Total de horas: ${data.total_horas}\nAsignaciones: ${data.asignaciones.length}`);
        },
        error: (error) => {
          console.error('Error al obtener asignaciones:', error);
        }
      });
    }
  }
}
