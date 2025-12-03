from fastapi import APIRouter
from app.models import ResultadoOptimizacion, CONFIGURACION
from app.services.optimizacion import optimizador
from app.database import db

router = APIRouter()

@router.post("/ejecutar", response_model=ResultadoOptimizacion)
def ejecutar_optimizacion():
    """
    Ejecuta el algoritmo de optimización para asignar docentes a grupos.
    Considera todas las restricciones:
    - Máximo 20 horas por docente
    - Máximo 2 grados diferentes por docente
    - Distribución por niveles en grados 4-11
    - Intensidad horaria según nivel
    """
    resultado = optimizador.optimizar_asignacion()
    
    # Guardar asignaciones en la base de datos
    for asignacion in resultado.asignaciones:
        db.agregar_asignacion(asignacion)
    
    return resultado

@router.get("/necesidades")
def calcular_necesidades():
    """
    Calcula las necesidades de horas y grupos a cubrir
    """
    necesidades = optimizador.calcular_necesidades()
    
    horas_totales = necesidades["primaria"]["horas_totales"] + necesidades["bachillerato"]["horas_totales"]
    docentes_ideales = horas_totales / CONFIGURACION["horas_maximas_docente"]
    docentes_actuales = len(db.docentes)
    
    return {
        "necesidades": necesidades,
        "horas_totales_necesarias": horas_totales,
        "docentes_actuales": docentes_actuales,
        "docentes_ideales": round(docentes_ideales, 2),
        "deficit_docentes": max(0, int(docentes_ideales) - docentes_actuales + 1)
    }

@router.get("/estadisticas")
def obtener_estadisticas():
    """
    Obtiene estadísticas generales del sistema
    """
    docentes = db.obtener_docentes()
    asignaciones = db.obtener_asignaciones()
    grupos = db.obtener_grupos()
    
    docentes_con_asignacion = len(set([a.docente_id for a in asignaciones]))
    horas_asignadas_total = sum([a.horas_semanales for a in asignaciones])
    
    # Distribución por tipo de docente
    dist_primaria = len([d for d in docentes if d.tipo.value == "primaria"])
    dist_bachillerato = len([d for d in docentes if d.tipo.value == "bachillerato"])
    
    return {
        "total_docentes": len(docentes),
        "docentes_primaria": dist_primaria,
        "docentes_bachillerato": dist_bachillerato,
        "docentes_utilizados": docentes_con_asignacion,
        "total_grupos": len(grupos),
        "total_asignaciones": len(asignaciones),
        "horas_asignadas_total": horas_asignadas_total,
        "promedio_horas_por_docente": round(horas_asignadas_total / docentes_con_asignacion, 2) if docentes_con_asignacion > 0 else 0
    }
