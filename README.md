# 📚 Gestor de Labor Docente

Sistema completo de gestión y optimización de asignación docente por niveles para instituciones educativas. Proyección 2026.

## 🎯 Descripción

Aplicación web que permite optimizar la distribución de docentes en grupos escolares considerando:
- Sistema de niveles (Básico e Intermedio) para grados 4° a 11°
- Restricciones de horas máximas (20h/semana por docente)
- Límite de grados diferentes por docente (máximo 2)
- Intensidad horaria diferenciada (5h primaria, 4h bachillerato)
- Grupos de aproximadamente 20 estudiantes por nivel
- Recomendaciones automáticas de contratación

## 🏗️ Arquitectura

### Backend - Python (FastAPI)
- ✅ API REST completa
- ✅ Algoritmo de optimización greedy
- ✅ Validación de restricciones
- ✅ Cálculo automático de necesidades
- ✅ Base de datos en memoria (migrable a PostgreSQL/MySQL)

### Frontend - Angular
- ✅ Interfaz moderna y responsive
- ✅ Dashboard con estadísticas en tiempo real
- ✅ Gestión completa de docentes
- ✅ Visualización de resultados de optimización
- ✅ Alertas y recomendaciones visuales

## 📊 Configuración del Colegio - Proyección 2026

| Grado | Grupos | Sistema | Niveles |
|-------|--------|---------|---------|
| Preescolar | 4 | Sin niveles | 1 docente/grupo |
| Primero | 4 | Sin niveles | 1 docente/grupo |
| Segundo | 4 | Sin niveles | 1 docente/grupo |
| Tercero | 4 | Sin niveles | 1 docente/grupo |
| Cuarto | 4 | Con niveles | Básico + Intermedio |
| Quinto | 6 | Con niveles | Básico + Intermedio |
| Sexto | 7 | Con niveles | Básico + Intermedio |
| Séptimo | 10 | Con niveles | Básico + Intermedio |
| Octavo | 10 | Con niveles | Básico + Intermedio |
| Noveno | 10 | Con niveles | Básico + Intermedio |
| Décimo | 10 | Con niveles | Básico + Intermedio |
| Undécimo | 10 | Con niveles | Básico + Intermedio |

**Total:** 83 grupos

### Recursos Docentes
- **Primaria:** 10 docentes
- **Bachillerato:** 11 docentes
- **Total:** 21 docentes

### Intensidad Horaria
- **Primaria (Preescolar - 5°):** 5 horas semanales
- **Bachillerato (6° - 11°):** 4 horas semanales

## 🚀 Instalación y Ejecución

### Prerrequisitos
- Python 3.8+
- Node.js 18+
- Angular CLI 19+

### Backend (FastAPI)

```bash
# Navegar a la carpeta backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn app.main:app --reload

# API disponible en: http://localhost:8000
# Documentación: http://localhost:8000/docs
```

### Frontend (Angular)

```bash
# Navegar a la carpeta frontend
cd frontend

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm start

# Aplicación disponible en: http://localhost:4200
```

## 📁 Estructura del Proyecto

```
LaborDoc/
├── backend/                    # Backend FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # Aplicación FastAPI
│   │   ├── models.py          # Modelos Pydantic
│   │   ├── database.py        # BD en memoria
│   │   ├── routes/            # Endpoints REST
│   │   │   ├── docentes.py
│   │   │   ├── grupos.py
│   │   │   ├── asignaciones.py
│   │   │   └── optimizacion.py
│   │   └── services/          # Lógica de negocio
│   │       └── optimizacion.py # Algoritmo
│   ├── requirements.txt
│   └── README.md
│
├── frontend/                   # Frontend Angular
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/
│   │   │   │   ├── dashboard/
│   │   │   │   ├── docentes/
│   │   │   │   └── optimizacion/
│   │   │   ├── models/        # Interfaces TypeScript
│   │   │   ├── services/      # Servicios HTTP
│   │   │   ├── app.component.*
│   │   │   ├── app.routes.ts
│   │   │   └── app.config.ts
│   │   └── styles.scss
│   ├── package.json
│   └── README.md
│
└── README.md                   # Este archivo
```

## 🔧 Funcionalidades Principales

### 1. Dashboard
- Vista general del sistema
- Estadísticas en tiempo real
- Análisis de necesidades 2026
- Configuración del sistema
- Acceso rápido a funcionalidades

### 2. Gestión de Docentes
- Crear, editar y eliminar docentes
- Asignar tipo (Primaria, Bachillerato, Ambos)
- Ver asignaciones actuales
- Control de horas (máximo 20h/semana)
- Indicadores visuales de disponibilidad

### 3. Optimización de Asignaciones
- Ejecutar algoritmo de optimización automática
- Visualizar distribución por docente
- Ver alertas de restricciones
- Calcular necesidades de contratación
- Limpiar y reiniciar asignaciones

## 🧮 Algoritmo de Optimización

El sistema utiliza un **algoritmo greedy** que:

1. **Calcula necesidades totales:**
   - Primaria: grupos × 5 horas
   - Bachillerato: grupos por nivel × 4 horas

2. **Agrupa por niveles (grados 4-11):**
   - Cada par de grupos genera 2 niveles
   - Ejemplo: 7°1 + 7°2 → Grupo Básico + Grupo Intermedio

3. **Asigna docentes priorizando:**
   - Docentes con menos horas asignadas
   - Docentes que ya tienen ese grado (para no exceder 2 grados)
   - Disponibilidad de horas restantes

4. **Valida restricciones:**
   - Máximo 20 horas por docente
   - Máximo 2 grados diferentes
   - Intensidad horaria correcta

5. **Genera recomendaciones:**
   - Indica si se necesitan más docentes
   - Calcula el déficit exacto
   - Muestra alertas de grupos sin cubrir

## 📊 API Endpoints

### Docentes
- `GET /api/docentes` - Listar todos
- `GET /api/docentes/{id}` - Obtener uno
- `POST /api/docentes` - Crear
- `PUT /api/docentes/{id}` - Actualizar
- `DELETE /api/docentes/{id}` - Eliminar
- `GET /api/docentes/{id}/asignaciones` - Ver asignaciones

### Grupos
- `GET /api/grupos` - Listar todos
- `GET /api/grupos/{id}` - Obtener uno
- `GET /api/grupos/grado/{grado}` - Por grado

### Optimización
- `POST /api/optimizacion/ejecutar` - Ejecutar optimización
- `GET /api/optimizacion/necesidades` - Calcular necesidades
- `GET /api/optimizacion/estadisticas` - Estadísticas generales

### Asignaciones
- `GET /api/asignaciones` - Listar todas
- `POST /api/asignaciones/limpiar` - Limpiar todas

## 🎨 Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno y rápido
- **Pydantic** - Validación de datos
- **Uvicorn** - Servidor ASGI

### Frontend
- **Angular 19** - Framework frontend
- **TypeScript** - Lenguaje tipado
- **SCSS** - Preprocesador CSS
- **RxJS** - Programación reactiva

## 💡 ¿Por qué Python en el Backend?

**Python es la mejor opción porque:**

1. **Optimización matemática:** Librerías como PuLP, OR-Tools, scipy.optimize
2. **Algoritmos complejos:** Mejor para problemas de scheduling y asignación de recursos
3. **Análisis de datos:** Pandas, NumPy para manipulación de datos
4. **Mantenibilidad:** Código más legible para lógica compleja
5. **Escalabilidad:** Fácil integración con ML/AI en el futuro

**vs Node.js:**
- Node es excelente para I/O intensivo
- Pero Python es superior para cálculos y optimización
- Este proyecto requiere más capacidad de cálculo que velocidad de I/O

## 🔮 Próximas Mejoras

- [ ] Base de datos PostgreSQL/MySQL
- [ ] Autenticación y roles de usuario
- [ ] Generación de horarios específicos (días/horas)
- [ ] Exportación a PDF/Excel
- [ ] Gráficos interactivos con Chart.js
- [ ] Sistema de notificaciones
- [ ] Historial de cambios
- [ ] Modo oscuro
- [ ] PWA (Progressive Web App)
- [ ] Tests unitarios y E2E

## 📝 Notas Importantes

1. **Base de datos en memoria:** Los datos se pierden al reiniciar el servidor. Para producción, migrar a PostgreSQL o MySQL.

2. **CORS:** El backend acepta peticiones desde `http://localhost:4200`. Ajustar para producción.

3. **Validaciones:** El sistema valida automáticamente todas las restricciones. No es posible asignar más de 20h o más de 2 grados por docente.

4. **Datos iniciales:** El sistema inicia con 10 docentes de primaria, 11 de bachillerato y todos los grupos configurados.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👥 Contacto

Para preguntas o soporte, por favor abre un issue en el repositorio.

---

**Desarrollado con ❤️ para optimizar la gestión educativa**
