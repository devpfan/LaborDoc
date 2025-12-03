"""
Servicio de optimización para la asignación de docentes.
Utiliza programación lineal para optimizar la distribución considerando todas las restricciones.
"""
from typing import List, Dict, Tuple
from app.models import (
    Docente, Grupo, Asignacion, ResultadoOptimizacion, 
    NivelEnum, TipoDocenteEnum, CONFIGURACION, GrupoNivel
)
from app.database import db
import itertools

class OptimizadorAsignaciones:
    
    def __init__(self):
        self.grados_primaria = CONFIGURACION["grados_sin_niveles"]
        self.grados_bachillerato = CONFIGURACION["grados_con_niveles"]
    
    def calcular_grupos_nivel(self, grado: str, num_grupos: int) -> List[GrupoNivel]:
        """
        Divide los grupos en niveles. Por ejemplo:
        - Séptimo con 10 grupos -> 5 básico + 5 intermedio
        - Cada nivel agrupa 2 grupos (ej: 7°1+7°2 = 1 grupo básico)
        """
        if grado in self.grados_primaria:
            return []
        
        # Cada par de grupos forma un nivel
        grupos_nivel = []
        grupos_por_nivel = num_grupos // 2
        
        # Grupos básico
        for i in range(grupos_por_nivel):
            grupos_origen = [i*2 + 1, i*2 + 2] if i*2 + 2 <= num_grupos else [i*2 + 1]
            grupos_nivel.append(GrupoNivel(
                grado=grado,
                grupos_origen=grupos_origen,
                nivel=NivelEnum.BASICO,
                estudiantes=20
            ))
        
        # Grupos intermedio
        for i in range(grupos_por_nivel):
            grupos_origen = [i*2 + 1, i*2 + 2] if i*2 + 2 <= num_grupos else [i*2 + 1]
            grupos_nivel.append(GrupoNivel(
                grado=grado,
                grupos_origen=grupos_origen,
                nivel=NivelEnum.INTERMEDIO,
                estudiantes=20
            ))
        
        return grupos_nivel
    
    def calcular_necesidades(self) -> Dict:
        """Calcula las horas totales necesarias y grupos a cubrir"""
        necesidades = {
            "primaria": {
                "grupos": 0,
                "horas_totales": 0,
                "grados": {}
            },
            "bachillerato": {
                "grupos_nivel": 0,
                "horas_totales": 0,
                "grados": {}
            }
        }
        
        for grado, num_grupos in CONFIGURACION["grupos_por_grado"].items():
            if grado in self.grados_primaria:
                # Primaria: 1 grupo = 1 asignación de 5 horas
                necesidades["primaria"]["grupos"] += num_grupos
                necesidades["primaria"]["horas_totales"] += num_grupos * CONFIGURACION["intensidad_horaria"]["primaria"]
                necesidades["primaria"]["grados"][grado] = num_grupos
            else:
                # Bachillerato: cada par de grupos genera 2 niveles
                grupos_nivel = self.calcular_grupos_nivel(grado, num_grupos)
                necesidades["bachillerato"]["grupos_nivel"] += len(grupos_nivel)
                necesidades["bachillerato"]["horas_totales"] += len(grupos_nivel) * CONFIGURACION["intensidad_horaria"]["bachillerato"]
                necesidades["bachillerato"]["grados"][grado] = len(grupos_nivel)
        
        return necesidades
    
    def optimizar_asignacion(self) -> ResultadoOptimizacion:
        """
        Realiza la asignación óptima de docentes considerando todas las restricciones
        """
        db.limpiar_asignaciones()
        
        necesidades = self.calcular_necesidades()
        asignaciones = []
        alertas = []
        
        # Obtener docentes disponibles
        docentes_primaria = [d for d in db.docentes if d.tipo in [TipoDocenteEnum.PRIMARIA, TipoDocenteEnum.AMBOS]]
        docentes_bachillerato = [d for d in db.docentes if d.tipo in [TipoDocenteEnum.BACHILLERATO, TipoDocenteEnum.AMBOS]]
        
        # 1. Asignar primaria (sin niveles)
        asignaciones_primaria, alertas_prim = self._asignar_primaria(docentes_primaria, necesidades["primaria"])
        asignaciones.extend(asignaciones_primaria)
        alertas.extend(alertas_prim)
        
        # 2. Asignar bachillerato (con niveles)
        asignaciones_bach, alertas_bach = self._asignar_bachillerato(docentes_bachillerato, necesidades["bachillerato"])
        asignaciones.extend(asignaciones_bach)
        alertas.extend(alertas_bach)
        
        # Calcular estadísticas
        docentes_utilizados = len(set([a.docente_id for a in asignaciones]))
        total_grupos_a_cubrir = necesidades["primaria"]["grupos"] + necesidades["bachillerato"]["grupos_nivel"]
        grupos_cubiertos = len(asignaciones)
        cobertura = (grupos_cubiertos / total_grupos_a_cubrir * 100) if total_grupos_a_cubrir > 0 else 0
        
        # Calcular si se necesitan más docentes
        horas_totales_necesarias = necesidades["primaria"]["horas_totales"] + necesidades["bachillerato"]["horas_totales"]
        horas_disponibles = len(db.docentes) * CONFIGURACION["horas_maximas_docente"]
        docentes_necesarios = int(horas_totales_necesarias / CONFIGURACION["horas_maximas_docente"]) + 1
        docentes_adicionales = max(0, docentes_necesarios - len(db.docentes))
        
        # Distribución por docente
        distribucion = {}
        for docente in db.docentes:
            asig_docente = [a for a in asignaciones if a.docente_id == docente.id]
            if asig_docente:
                distribucion[docente.nombre] = {
                    "horas": sum([a.horas_semanales for a in asig_docente]),
                    "grupos": len(asig_docente),
                    "grados": list(set([a.grado.value for a in asig_docente]))
                }
        
        return ResultadoOptimizacion(
            asignaciones=asignaciones,
            docentes_utilizados=docentes_utilizados,
            docentes_necesarios=docentes_necesarios,
            requiere_contratar=docentes_adicionales > 0,
            docentes_adicionales=docentes_adicionales,
            cobertura_total=round(cobertura, 2),
            alertas=alertas,
            distribucion_por_docente=distribucion
        )
    
    def _asignar_primaria(self, docentes: List[Docente], necesidades: Dict) -> Tuple[List[Asignacion], List[str]]:
        """Asigna grupos de primaria a docentes disponibles"""
        asignaciones = []
        alertas = []
        docentes_disponibles = sorted(docentes, key=lambda d: d.horas_asignadas)
        
        for grado, num_grupos in necesidades["grados"].items():
            grupos = db.obtener_grupos_por_grado(grado)
            
            for grupo in grupos[:num_grupos]:
                # Buscar docente con menos horas y que no tenga más de 2 grados
                docente_asignado = None
                
                for docente in docentes_disponibles:
                    horas_restantes = CONFIGURACION["horas_maximas_docente"] - docente.horas_asignadas
                    puede_asignar = horas_restantes >= CONFIGURACION["intensidad_horaria"]["primaria"]
                    grados_diferentes = len(set(docente.grados_asignados))
                    
                    if puede_asignar and (grado in docente.grados_asignados or grados_diferentes < 2):
                        docente_asignado = docente
                        break
                
                if docente_asignado:
                    asignacion = Asignacion(
                        docente_id=docente_asignado.id,
                        grupo_id=grupo.id,
                        grado=grado,
                        nivel=NivelEnum.UNICO,
                        horas_semanales=CONFIGURACION["intensidad_horaria"]["primaria"]
                    )
                    asignaciones.append(asignacion)
                    
                    # Actualizar docente
                    docente_asignado.horas_asignadas += CONFIGURACION["intensidad_horaria"]["primaria"]
                    if grado not in docente_asignado.grados_asignados:
                        docente_asignado.grados_asignados.append(grado)
                    
                    # Re-ordenar
                    docentes_disponibles = sorted(docentes_disponibles, key=lambda d: d.horas_asignadas)
                else:
                    alertas.append(f"No hay docentes disponibles para {grado} grupo {grupo.numero_grupo}")
        
        return asignaciones, alertas
    
    def _asignar_bachillerato(self, docentes: List[Docente], necesidades: Dict) -> Tuple[List[Asignacion], List[str]]:
        """Asigna grupos de bachillerato por niveles"""
        asignaciones = []
        alertas = []
        docentes_disponibles = sorted(docentes, key=lambda d: d.horas_asignadas)
        
        for grado, num_grupos_nivel in necesidades["grados"].items():
            num_grupos_original = CONFIGURACION["grupos_por_grado"][grado]
            grupos_nivel = self.calcular_grupos_nivel(grado, num_grupos_original)
            
            for grupo_nivel in grupos_nivel:
                # Buscar docente disponible
                docente_asignado = None
                
                for docente in docentes_disponibles:
                    horas_restantes = CONFIGURACION["horas_maximas_docente"] - docente.horas_asignadas
                    puede_asignar = horas_restantes >= CONFIGURACION["intensidad_horaria"]["bachillerato"]
                    grados_diferentes = len(set(docente.grados_asignados))
                    
                    if puede_asignar and (grado in docente.grados_asignados or grados_diferentes < 2):
                        docente_asignado = docente
                        break
                
                if docente_asignado:
                    asignacion = Asignacion(
                        docente_id=docente_asignado.id,
                        grado=grado,
                        nivel=grupo_nivel.nivel,
                        horas_semanales=CONFIGURACION["intensidad_horaria"]["bachillerato"]
                    )
                    asignaciones.append(asignacion)
                    
                    # Actualizar docente
                    docente_asignado.horas_asignadas += CONFIGURACION["intensidad_horaria"]["bachillerato"]
                    if grado not in docente_asignado.grados_asignados:
                        docente_asignado.grados_asignados.append(grado)
                    
                    docentes_disponibles = sorted(docentes_disponibles, key=lambda d: d.horas_asignadas)
                else:
                    alertas.append(f"No hay docentes disponibles para {grado} nivel {grupo_nivel.nivel.value}")
        
        return asignaciones, alertas

# Instancia global del optimizador
optimizador = OptimizadorAsignaciones()
