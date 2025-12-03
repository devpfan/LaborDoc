"""
Almacenamiento de configuración dinámica del sistema
"""
from app.models import ConfiguracionColegio, CONFIGURACION

class ConfiguracionStore:
    def __init__(self):
        # Configuración actual (inicializa con valores por defecto)
        self.configuracion = ConfiguracionColegio(
            grupos_por_grado=CONFIGURACION["grupos_por_grado"].copy(),
            intensidad_horaria_primaria=CONFIGURACION["intensidad_horaria"]["primaria"],
            intensidad_horaria_bachillerato=CONFIGURACION["intensidad_horaria"]["bachillerato"],
            horas_maximas_docente=CONFIGURACION["horas_maximas_docente"],
            estudiantes_por_grupo_nivel=CONFIGURACION["estudiantes_por_grupo_nivel"],
            grados_sin_niveles=CONFIGURACION["grados_sin_niveles"].copy(),
            grados_con_niveles=CONFIGURACION["grados_con_niveles"].copy()
        )
    
    def obtener_configuracion(self) -> ConfiguracionColegio:
        """Obtiene la configuración actual"""
        return self.configuracion
    
    def actualizar_configuracion(self, nueva_config: ConfiguracionColegio) -> ConfiguracionColegio:
        """Actualiza la configuración del sistema"""
        self.configuracion = nueva_config
        
        # Actualizar CONFIGURACION global para mantener compatibilidad
        CONFIGURACION["grupos_por_grado"] = nueva_config.grupos_por_grado
        CONFIGURACION["intensidad_horaria"]["primaria"] = nueva_config.intensidad_horaria_primaria
        CONFIGURACION["intensidad_horaria"]["bachillerato"] = nueva_config.intensidad_horaria_bachillerato
        CONFIGURACION["horas_maximas_docente"] = nueva_config.horas_maximas_docente
        CONFIGURACION["estudiantes_por_grupo_nivel"] = nueva_config.estudiantes_por_grupo_nivel
        CONFIGURACION["grados_sin_niveles"] = nueva_config.grados_sin_niveles
        CONFIGURACION["grados_con_niveles"] = nueva_config.grados_con_niveles
        
        return self.configuracion
    
    def resetear_configuracion(self) -> ConfiguracionColegio:
        """Resetea la configuración a valores por defecto"""
        self.configuracion = ConfiguracionColegio()
        return self.configuracion

# Instancia global del store de configuración
config_store = ConfiguracionStore()
