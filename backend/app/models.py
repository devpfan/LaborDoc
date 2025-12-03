from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal
from enum import Enum

class NivelEnum(str, Enum):
    UNICO = "unico"  # Preescolar a 3°
    BASICO = "basico"  # 4° a 11°
    INTERMEDIO = "intermedio"  # 4° a 11°

class TipoDocenteEnum(str, Enum):
    PRIMARIA = "primaria"
    BACHILLERATO = "bachillerato"
    AMBOS = "ambos"

class Grado(str, Enum):
    PREESCOLAR = "Preescolar"
    PRIMERO = "Primero"
    SEGUNDO = "Segundo"
    TERCERO = "Tercero"
    CUARTO = "Cuarto"
    QUINTO = "Quinto"
    SEXTO = "Sexto"
    SEPTIMO = "Séptimo"
    OCTAVO = "Octavo"
    NOVENO = "Noveno"
    DECIMO = "Décimo"
    UNDECIMO = "Undécimo"

# Configuración del colegio
CONFIGURACION = {
    "grupos_por_grado": {
        "Preescolar": 4,
        "Primero": 4,
        "Segundo": 4,
        "Tercero": 4,
        "Cuarto": 4,
        "Quinto": 6,
        "Sexto": 7,
        "Séptimo": 10,
        "Octavo": 10,
        "Noveno": 10,
        "Décimo": 10,
        "Undécimo": 10
    },
    "intensidad_horaria": {
        "primaria": 5,  # horas semanales
        "bachillerato": 4  # horas semanales
    },
    "horas_maximas_docente": 20,
    "estudiantes_por_grupo_nivel": 20,
    "grados_sin_niveles": ["Preescolar", "Primero", "Segundo", "Tercero"],
    "grados_con_niveles": ["Cuarto", "Quinto", "Sexto", "Séptimo", "Octavo", "Noveno", "Décimo", "Undécimo"]
}

class Docente(BaseModel):
    id: Optional[int] = None
    nombre: str
    tipo: TipoDocenteEnum
    horas_asignadas: int = 0
    grados_asignados: List[str] = []
    disponible: bool = True
    
    @validator('horas_asignadas')
    def validar_horas(cls, v):
        if v > CONFIGURACION["horas_maximas_docente"]:
            raise ValueError(f'Las horas no pueden exceder {CONFIGURACION["horas_maximas_docente"]}')
        return v

class Grupo(BaseModel):
    id: Optional[int] = None
    grado: Grado
    numero_grupo: int  # 1, 2, 3, etc.
    nivel: Optional[NivelEnum] = None
    estudiantes: int = 20
    horario_asignado: Optional[List[str]] = []
    
    @property
    def nombre_completo(self) -> str:
        return f"{self.grado} {self.numero_grupo}"
    
    @property
    def requiere_niveles(self) -> bool:
        return self.grado.value in CONFIGURACION["grados_con_niveles"]

class GrupoNivel(BaseModel):
    """Representa un grupo dividido por nivel (para grados 4-11)"""
    grado: Grado
    grupos_origen: List[int]  # ej: [1, 2] significa 7°1 y 7°2
    nivel: NivelEnum
    estudiantes: int
    
    @property
    def nombre(self) -> str:
        grupos_str = "+".join([str(g) for g in self.grupos_origen])
        return f"{self.grado} ({grupos_str}) - {self.nivel.value.title()}"

class Asignacion(BaseModel):
    id: Optional[int] = None
    docente_id: int
    grupo_id: Optional[int] = None  # Para grados sin niveles
    grupo_nivel_id: Optional[int] = None  # Para grados con niveles
    grado: Grado
    nivel: Optional[NivelEnum] = None
    horas_semanales: int
    dia_semana: Optional[str] = None
    hora_inicio: Optional[str] = None
    
class ResultadoOptimizacion(BaseModel):
    asignaciones: List[Asignacion]
    docentes_utilizados: int
    docentes_necesarios: int
    requiere_contratar: bool
    docentes_adicionales: int
    cobertura_total: float
    alertas: List[str] = []
    distribucion_por_docente: dict = {}
    
class ConfiguracionColegio(BaseModel):
    """Configuración editable del colegio"""
    grupos_por_grado: dict = {
        "Preescolar": 4,
        "Primero": 4,
        "Segundo": 4,
        "Tercero": 4,
        "Cuarto": 4,
        "Quinto": 6,
        "Sexto": 7,
        "Séptimo": 10,
        "Octavo": 10,
        "Noveno": 10,
        "Décimo": 10,
        "Undécimo": 10
    }
    intensidad_horaria_primaria: int = 5
    intensidad_horaria_bachillerato: int = 4
    horas_maximas_docente: int = 20
    estudiantes_por_grupo_nivel: int = 20
    numero_docentes_primaria: int = 10
    numero_docentes_bachillerato: int = 11
    grados_sin_niveles: List[str] = ["Preescolar", "Primero", "Segundo", "Tercero"]
    grados_con_niveles: List[str] = ["Cuarto", "Quinto", "Sexto", "Séptimo", "Octavo", "Noveno", "Décimo", "Undécimo"]
