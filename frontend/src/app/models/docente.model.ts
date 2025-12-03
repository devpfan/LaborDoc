export enum TipoDocente {
  PRIMARIA = 'primaria',
  BACHILLERATO = 'bachillerato',
  AMBOS = 'ambos'
}

export enum Nivel {
  UNICO = 'unico',
  BASICO = 'basico',
  INTERMEDIO = 'intermedio'
}

export interface Docente {
  id?: number;
  nombre: string;
  tipo: TipoDocente;
  horas_asignadas: number;
  grados_asignados: string[];
  disponible: boolean;
}

export interface Grupo {
  id?: number;
  grado: string;
  numero_grupo: number;
  nivel?: Nivel;
  estudiantes: number;
  horario_asignado?: string[];
}

export interface Asignacion {
  id?: number;
  docente_id: number;
  grupo_id?: number;
  grupo_nivel_id?: number;
  grado: string;
  nivel?: Nivel;
  horas_semanales: number;
  dia_semana?: string;
  hora_inicio?: string;
}

export interface ResultadoOptimizacion {
  asignaciones: Asignacion[];
  docentes_utilizados: number;
  docentes_necesarios: number;
  requiere_contratar: boolean;
  docentes_adicionales: number;
  cobertura_total: number;
  alertas: string[];
  distribucion_por_docente: { [key: string]: any };
}

export interface Estadisticas {
  total_docentes: number;
  docentes_primaria: number;
  docentes_bachillerato: number;
  docentes_utilizados: number;
  total_grupos: number;
  total_asignaciones: number;
  horas_asignadas_total: number;
  promedio_horas_por_docente: number;
}

export interface ConfiguracionColegio {
  grupos_por_grado: { [key: string]: number };
  intensidad_horaria_primaria: number;
  intensidad_horaria_bachillerato: number;
  horas_maximas_docente: number;
  estudiantes_por_grupo_nivel: number;
  numero_docentes_primaria?: number;
  numero_docentes_bachillerato?: number;
  grados_sin_niveles: string[];
  grados_con_niveles: string[];
}
