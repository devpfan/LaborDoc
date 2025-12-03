from fastapi import APIRouter
from app.models import ConfiguracionColegio
from app.config_store import config_store
from app.database import db

router = APIRouter()

@router.get("/", response_model=ConfiguracionColegio)
def obtener_configuracion():
    """Obtiene la configuración actual del sistema"""
    return config_store.obtener_configuracion()

@router.put("/", response_model=ConfiguracionColegio)
def actualizar_configuracion(config: ConfiguracionColegio):
    """
    Actualiza la configuración del sistema.
    IMPORTANTE: Esto afectará el cálculo de necesidades y la optimización.
    """
    # Actualizar configuración
    nueva_config = config_store.actualizar_configuracion(config)
    
    # Limpiar asignaciones ya que la configuración cambió
    db.limpiar_asignaciones()
    
    # Regenerar grupos si cambiaron los números
    db._inicializar_grupos()
    
    return nueva_config

@router.post("/resetear", response_model=ConfiguracionColegio)
def resetear_configuracion():
    """Resetea la configuración a los valores por defecto"""
    config = config_store.resetear_configuracion()
    
    # Limpiar asignaciones y regenerar grupos
    db.limpiar_asignaciones()
    db._inicializar_grupos()
    
    return config

@router.get("/validar")
def validar_configuracion():
    """
    Valida la configuración actual y devuelve advertencias o errores
    """
    config = config_store.obtener_configuracion()
    advertencias = []
    errores = []
    
    # Validar que haya grupos definidos
    total_grupos = sum(config.grupos_por_grado.values())
    if total_grupos == 0:
        errores.append("No hay grupos definidos")
    
    # Validar intensidad horaria
    if config.intensidad_horaria_primaria <= 0:
        errores.append("La intensidad horaria de primaria debe ser mayor a 0")
    if config.intensidad_horaria_bachillerato <= 0:
        errores.append("La intensidad horaria de bachillerato debe ser mayor a 0")
    
    # Validar horas máximas
    if config.horas_maximas_docente <= 0:
        errores.append("Las horas máximas por docente deben ser mayor a 0")
    
    if config.horas_maximas_docente < max(config.intensidad_horaria_primaria, config.intensidad_horaria_bachillerato):
        advertencias.append("Las horas máximas por docente son menores que la intensidad horaria")
    
    # Calcular horas totales necesarias
    grupos_primaria = sum([config.grupos_por_grado.get(g, 0) for g in config.grados_sin_niveles])
    grupos_bachillerato = sum([config.grupos_por_grado.get(g, 0) for g in config.grados_con_niveles])
    
    horas_primaria = grupos_primaria * config.intensidad_horaria_primaria
    # En bachillerato cada grupo genera 2 niveles
    horas_bachillerato = grupos_bachillerato * 2 * config.intensidad_horaria_bachillerato
    
    horas_totales = horas_primaria + horas_bachillerato
    docentes_necesarios = horas_totales / config.horas_maximas_docente
    
    total_docentes = len(db.docentes)
    
    if docentes_necesarios > total_docentes:
        advertencias.append(f"Se necesitan aproximadamente {int(docentes_necesarios)} docentes, pero solo hay {total_docentes} registrados")
    
    return {
        "valida": len(errores) == 0,
        "errores": errores,
        "advertencias": advertencias,
        "estadisticas": {
            "total_grupos": total_grupos,
            "grupos_primaria": grupos_primaria,
            "grupos_bachillerato": grupos_bachillerato,
            "horas_totales_necesarias": horas_totales,
            "docentes_necesarios_aproximados": round(docentes_necesarios, 2),
            "docentes_registrados": total_docentes
        }
    }
