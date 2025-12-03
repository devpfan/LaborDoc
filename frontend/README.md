# Gestor de Labor Docente - Frontend

Frontend del sistema de gestión y optimización de asignación docente por niveles construido con Angular.

## Características

- ✅ Interfaz moderna y responsive
- ✅ Dashboard con estadísticas en tiempo real
- ✅ Gestión completa de docentes (CRUD)
- ✅ Optimización visual de asignaciones
- ✅ Gráficos y visualización de datos
- ✅ Alertas y recomendaciones automáticas

## Requisitos Previos

- Node.js >= 18.x
- Angular CLI >= 19.x

```bash
npm install -g @angular/cli
```

## Instalación

```bash
# Instalar dependencias
cd frontend
npm install
```

## Ejecución en Desarrollo

```bash
# Iniciar el servidor de desarrollo
npm start

# La aplicación estará disponible en http://localhost:4200
```

## Compilación para Producción

```bash
# Compilar para producción
npm run build

# Los archivos compilados estarán en dist/
```

## Estructura del Proyecto

```
frontend/
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   ├── dashboard/         # Dashboard principal
│   │   │   ├── docentes/          # Gestión de docentes
│   │   │   └── optimizacion/      # Optimización y resultados
│   │   ├── models/                # Interfaces y modelos
│   │   ├── services/              # Servicios para API
│   │   ├── app.component.*        # Componente raíz
│   │   ├── app.routes.ts          # Configuración de rutas
│   │   └── app.config.ts          # Configuración de la app
│   ├── styles.scss                # Estilos globales
│   └── index.html                 # HTML principal
├── package.json
└── README.md
```

## Funcionalidades

### Dashboard
- Vista general del sistema
- Estadísticas en tiempo real
- Análisis de necesidades 2026
- Acciones rápidas
- Configuración del sistema

### Gestión de Docentes
- Crear, editar y eliminar docentes
- Asignar tipo (Primaria, Bachillerato, Ambos)
- Ver asignaciones por docente
- Indicadores visuales de disponibilidad
- Control de horas asignadas (max 20h)

### Optimización
- Ejecutar algoritmo de optimización
- Visualizar resultados detallados
- Distribución por docente
- Alertas y recomendaciones
- Cálculo de necesidades de contratación
- Limpiar asignaciones

## Componentes Principales

### Dashboard Component
```typescript
Ruta: /
Características:
- Tarjetas informativas con estadísticas
- Acciones rápidas para navegación
- Análisis de necesidades
- Información de configuración
```

### Docentes Component
```typescript
Ruta: /docentes
Características:
- Tabla de docentes con filtros
- Formulario de creación/edición
- Badges para tipos de docente
- Indicadores de horas (20h máx)
- Grados asignados
```

### Optimización Component
```typescript
Ruta: /optimizacion
Características:
- Botón de ejecución de optimización
- Resultados visuales
- Distribución por docente
- Alertas de restricciones
- Recomendaciones de contratación
```

## Servicios

### ApiService
```typescript
Métodos disponibles:
- getDocentes(): Observable<Docente[]>
- createDocente(docente): Observable<Docente>
- updateDocente(id, docente): Observable<Docente>
- deleteDocente(id): Observable<any>
- ejecutarOptimizacion(): Observable<ResultadoOptimizacion>
- getEstadisticas(): Observable<Estadisticas>
- getNecesidades(): Observable<any>
- limpiarAsignaciones(): Observable<any>
```

## Modelos de Datos

```typescript
interface Docente {
  id?: number;
  nombre: string;
  tipo: TipoDocente;
  horas_asignadas: number;
  grados_asignados: string[];
  disponible: boolean;
}

interface ResultadoOptimizacion {
  asignaciones: Asignacion[];
  docentes_utilizados: number;
  docentes_necesarios: number;
  requiere_contratar: boolean;
  docentes_adicionales: number;
  cobertura_total: number;
  alertas: string[];
  distribucion_por_docente: any;
}
```

## Estilos

El proyecto utiliza SCSS con:
- Variables de colores personalizadas
- Gradientes modernos
- Animaciones y transiciones
- Diseño responsive (mobile-first)
- Componentes reutilizables

## Conexión con Backend

El frontend se conecta al backend FastAPI en:
- **URL Base**: `http://localhost:8000/api`
- **CORS**: Configurado para permitir conexiones desde `http://localhost:4200`

## Desarrollo

### Crear un nuevo componente
```bash
ng generate component components/nombre-componente
```

### Crear un nuevo servicio
```bash
ng generate service services/nombre-servicio
```

## Testing

```bash
# Ejecutar tests unitarios
npm test

# Ejecutar tests con coverage
npm run test:coverage
```

## Próximas Mejoras

- [ ] Gráficos interactivos con Chart.js
- [ ] Exportación de reportes a PDF/Excel
- [ ] Sistema de notificaciones en tiempo real
- [ ] Modo oscuro
- [ ] Filtros avanzados y búsqueda
- [ ] Gestión de horarios específicos (días/horas)
- [ ] Historial de cambios
- [ ] Autenticación y roles de usuario

## Soporte

Para reportar problemas o sugerencias, por favor crea un issue en el repositorio.
