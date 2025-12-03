import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { 
  Docente, 
  Grupo, 
  Asignacion, 
  ResultadoOptimizacion,
  Estadisticas,
  ConfiguracionColegio
} from '../models/docente.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  // Docentes
  getDocentes(): Observable<Docente[]> {
    return this.http.get<Docente[]>(`${this.apiUrl}/docentes`);
  }

  getDocente(id: number): Observable<Docente> {
    return this.http.get<Docente>(`${this.apiUrl}/docentes/${id}`);
  }

  createDocente(docente: Docente): Observable<Docente> {
    return this.http.post<Docente>(`${this.apiUrl}/docentes`, docente);
  }

  updateDocente(id: number, docente: Docente): Observable<Docente> {
    return this.http.put<Docente>(`${this.apiUrl}/docentes/${id}`, docente);
  }

  deleteDocente(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/docentes/${id}`);
  }

  getAsignacionesDocente(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/docentes/${id}/asignaciones`);
  }

  // Grupos
  getGrupos(): Observable<Grupo[]> {
    return this.http.get<Grupo[]>(`${this.apiUrl}/grupos`);
  }

  getGruposPorGrado(grado: string): Observable<Grupo[]> {
    return this.http.get<Grupo[]>(`${this.apiUrl}/grupos/grado/${grado}`);
  }

  // Asignaciones
  getAsignaciones(): Observable<Asignacion[]> {
    return this.http.get<Asignacion[]>(`${this.apiUrl}/asignaciones`);
  }

  limpiarAsignaciones(): Observable<any> {
    return this.http.post(`${this.apiUrl}/asignaciones/limpiar`, {});
  }

  // Optimización
  ejecutarOptimizacion(): Observable<ResultadoOptimizacion> {
    return this.http.post<ResultadoOptimizacion>(`${this.apiUrl}/optimizacion/ejecutar`, {});
  }

  getNecesidades(): Observable<any> {
    return this.http.get(`${this.apiUrl}/optimizacion/necesidades`);
  }

  getEstadisticas(): Observable<Estadisticas> {
    return this.http.get<Estadisticas>(`${this.apiUrl}/optimizacion/estadisticas`);
  }

  // Configuración
  getConfiguracion(): Observable<ConfiguracionColegio> {
    return this.http.get<ConfiguracionColegio>(`${this.apiUrl}/configuracion`);
  }

  updateConfiguracion(config: ConfiguracionColegio): Observable<ConfiguracionColegio> {
    return this.http.put<ConfiguracionColegio>(`${this.apiUrl}/configuracion`, config);
  }

  resetearConfiguracion(): Observable<ConfiguracionColegio> {
    return this.http.post<ConfiguracionColegio>(`${this.apiUrl}/configuracion/resetear`, {});
  }

  validarConfiguracion(): Observable<any> {
    return this.http.get(`${this.apiUrl}/configuracion/validar`);
  }
}
