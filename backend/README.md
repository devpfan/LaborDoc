# Gestor de Labor Docente - Backend

Backend del sistema de gestión y optimización de asignación docente por niveles.

## Características

- ✅ API REST con FastAPI
- ✅ Algoritmo de optimización de asignaciones
- ✅ Sistema de niveles (básico/intermedio) para grados 4-11
- ✅ Validación automática de restricciones
- ✅ Cálculo de necesidades de contratación
- ✅ Distribución inteligente de horarios

## Restricciones implementadas

1. **Máximo 20 horas semanales** por docente
2. **Máximo 2 grados diferentes** por docente
3. **Intensidad horaria**:
   - Primaria: 5 horas semanales
   - Bachillerato: 4 horas semanales
4. **Grupos por nivel** (~20 estudiantes)
5. **Grados sin niveles**: Preescolar a 3°
6. **Grados con niveles**: 4° a 11° (Básico e Intermedio)

## Instalación

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en: `http://localhost:8000`

## Documentación API

Una vez iniciado el servidor, accede a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints principales

### Docentes
- `GET /api/docentes` - Listar todos los docentes
- `POST /api/docentes` - Crear docente
- `GET /api/docentes/{id}` - Obtener docente
- `PUT /api/docentes/{id}` - Actualizar docente
- `DELETE /api/docentes/{id}` - Eliminar docente

### Grupos
- `GET /api/grupos` - Listar todos los grupos
- `GET /api/grupos/grado/{grado}` - Grupos por grado
- `POST /api/grupos` - Crear grupo

### Optimización
- `POST /api/optimizacion/ejecutar` - Ejecutar algoritmo de optimización
- `GET /api/optimizacion/necesidades` - Calcular necesidades de docentes
- `GET /api/optimizacion/estadisticas` - Estadísticas generales

### Asignaciones
- `GET /api/asignaciones` - Listar asignaciones
- `POST /api/asignaciones/limpiar` - Limpiar asignaciones

## Configuración

El archivo `app/models.py` contiene la configuración del colegio:

```python
CONFIGURACION = {
    "grupos_por_grado": {
        "Preescolar": 4,
        "Primero": 4,
        # ... etc
    },
    "intensidad_horaria": {
        "primaria": 5,
        "bachillerato": 4
    },
    "horas_maximas_docente": 20,
    # ...
}
```

## Estructura del proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación FastAPI
│   ├── models.py            # Modelos de datos
│   ├── database.py          # Simulación de BD
│   ├── routes/              # Endpoints
│   │   ├── docentes.py
│   │   ├── grupos.py
│   │   ├── asignaciones.py
│   │   └── optimizacion.py
│   └── services/            # Lógica de negocio
│       └── optimizacion.py  # Algoritmo de optimización
├── requirements.txt
└── README.md
```

## Algoritmo de optimización

El sistema utiliza un algoritmo greedy que:

1. Calcula las necesidades totales de horas
2. Agrupa los grupos por niveles (en grados 4-11)
3. Asigna docentes priorizando:
   - Docentes con menos horas asignadas
   - Docentes que ya tienen ese grado (para no exceder 2 grados)
   - Disponibilidad de horas
4. Genera recomendaciones de contratación si es necesario

## Datos iniciales

El sistema inicia con:
- **10 docentes de primaria**
- **11 docentes de bachillerato**
- **Grupos configurados según la proyección 2026**

## Próximas mejoras

- [ ] Integración con base de datos PostgreSQL
- [ ] Generación de horarios específicos (días/horas)
- [ ] Exportación a PDF/Excel
- [ ] Sistema de notificaciones
- [ ] Historial de asignaciones
