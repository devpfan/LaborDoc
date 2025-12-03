"""
Simulación de base de datos en memoria.
En producción, se puede migrar a PostgreSQL, MySQL o MongoDB.
"""
from typing import List, Dict, Optional
from app.models import Docente, Grupo, Asignacion, TipoDocenteEnum, NivelEnum, CONFIGURACION

class Database:
    def __init__(self):
        self.docentes: List[Docente] = []
        self.grupos: List[Grupo] = []
        self.asignaciones: List[Asignacion] = []
        self._docente_counter = 1
        self._grupo_counter = 1
        self._asignacion_counter = 1
        
        # Inicializar con datos por defecto
        self._inicializar_docentes()
        self._inicializar_grupos()
    
    def _inicializar_docentes(self):
        """Crear los 10 docentes de primaria y 11 de bachillerato"""
        # Docentes de primaria
        for i in range(1, 11):
            self.agregar_docente(Docente(
                nombre=f"Docente Primaria {i}",
                tipo=TipoDocenteEnum.PRIMARIA
            ))
        
        # Docentes de bachillerato
        for i in range(1, 12):
            self.agregar_docente(Docente(
                nombre=f"Docente Bachillerato {i}",
                tipo=TipoDocenteEnum.BACHILLERATO
            ))
    
    def _inicializar_grupos(self):
        """Crear grupos según la configuración"""
        for grado, num_grupos in CONFIGURACION["grupos_por_grado"].items():
            for num in range(1, num_grupos + 1):
                self.agregar_grupo(Grupo(
                    grado=grado,
                    numero_grupo=num,
                    estudiantes=20
                ))
    
    # CRUD Docentes
    def agregar_docente(self, docente: Docente) -> Docente:
        docente.id = self._docente_counter
        self._docente_counter += 1
        self.docentes.append(docente)
        return docente
    
    def obtener_docentes(self) -> List[Docente]:
        return self.docentes
    
    def obtener_docente(self, docente_id: int) -> Optional[Docente]:
        for docente in self.docentes:
            if docente.id == docente_id:
                return docente
        return None
    
    def actualizar_docente(self, docente_id: int, docente_actualizado: Docente) -> Optional[Docente]:
        for i, docente in enumerate(self.docentes):
            if docente.id == docente_id:
                docente_actualizado.id = docente_id
                self.docentes[i] = docente_actualizado
                return docente_actualizado
        return None
    
    def eliminar_docente(self, docente_id: int) -> bool:
        for i, docente in enumerate(self.docentes):
            if docente.id == docente_id:
                del self.docentes[i]
                return True
        return False
    
    # CRUD Grupos
    def agregar_grupo(self, grupo: Grupo) -> Grupo:
        grupo.id = self._grupo_counter
        self._grupo_counter += 1
        self.grupos.append(grupo)
        return grupo
    
    def obtener_grupos(self) -> List[Grupo]:
        return self.grupos
    
    def obtener_grupo(self, grupo_id: int) -> Optional[Grupo]:
        for grupo in self.grupos:
            if grupo.id == grupo_id:
                return grupo
        return None
    
    def obtener_grupos_por_grado(self, grado: str) -> List[Grupo]:
        return [g for g in self.grupos if g.grado.value == grado]
    
    # CRUD Asignaciones
    def agregar_asignacion(self, asignacion: Asignacion) -> Asignacion:
        asignacion.id = self._asignacion_counter
        self._asignacion_counter += 1
        self.asignaciones.append(asignacion)
        return asignacion
    
    def obtener_asignaciones(self) -> List[Asignacion]:
        return self.asignaciones
    
    def limpiar_asignaciones(self):
        """Limpia todas las asignaciones y resetea las horas de los docentes"""
        self.asignaciones = []
        for docente in self.docentes:
            docente.horas_asignadas = 0
            docente.grados_asignados = []
            docente.disponible = True
    
    def obtener_asignaciones_docente(self, docente_id: int) -> List[Asignacion]:
        return [a for a in self.asignaciones if a.docente_id == docente_id]

# Instancia global de la base de datos
db = Database()
