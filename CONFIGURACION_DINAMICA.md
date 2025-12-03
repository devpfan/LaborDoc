# ⚙️ Configuración Dinámica del Sistema

## ✅ Nueva Funcionalidad Implementada

He agregado un sistema completo de **configuración dinámica** que permite modificar todos los parámetros del colegio sin necesidad de editar código.

## 🎯 Parámetros Configurables

### 📊 Grupos por Grado
- Preescolar a Undécimo
- Ajustable individualmente para cada grado
- Indicador visual de grados con/sin niveles

### ⏰ Intensidad Horaria
- **Primaria**: Horas semanales (por defecto: 5h)
- **Bachillerato**: Horas semanales (por defecto: 4h)

### 👥 Recursos Docentes
- **Horas máximas por docente**: (por defecto: 20h/semana)
- **Estudiantes por grupo/nivel**: (por defecto: 20)

## 🔧 Backend - Nuevos Endpoints

### GET `/api/configuracion`
Obtiene la configuración actual del sistema.

```json
{
  "grupos_por_grado": {
    "Preescolar": 4,
    "Primero": 4,
    ...
  },
  "intensidad_horaria_primaria": 5,
  "intensidad_horaria_bachillerato": 4,
  "horas_maximas_docente": 20,
  "estudiantes_por_grupo_nivel": 20,
  "grados_sin_niveles": ["Preescolar", "Primero", "Segundo", "Tercero"],
  "grados_con_niveles": ["Cuarto", "Quinto", ..., "Undécimo"]
}
```

### PUT `/api/configuracion`
Actualiza la configuración del sistema.
- **IMPORTANTE**: Limpia todas las asignaciones existentes
- Regenera los grupos según la nueva configuración

### POST `/api/configuracion/resetear`
Resetea la configuración a valores por defecto.

### GET `/api/configuracion/validar`
Valida la configuración actual y devuelve:
- ✅ **Estado**: Válida/Inválida
- ⚠️ **Advertencias**: Posibles problemas
- ❌ **Errores**: Problemas críticos
- 📊 **Estadísticas**: Análisis de necesidades

Ejemplo de respuesta:
```json
{
  "valida": true,
  "errores": [],
  "advertencias": [
    "Se necesitan aproximadamente 22 docentes, pero solo hay 21 registrados"
  ],
  "estadisticas": {
    "total_grupos": 83,
    "grupos_primaria": 16,
    "grupos_bachillerato": 67,
    "horas_totales_necesarias": 348,
    "docentes_necesarios_aproximados": 17.4,
    "docentes_registrados": 21
  }
}
```

## 💻 Frontend - Nuevo Componente

### Ruta: `/configuracion`

**Características:**
- ✅ Visualización de configuración actual
- ✏️ Edición de todos los parámetros
- 🔄 Reseteo a valores por defecto
- ✓ Validación en tiempo real
- ⚠️ Alertas y advertencias
- 📊 Estadísticas de necesidades

**Secciones:**

1. **Estado de Configuración**
   - Badge de validación (Válida/Inválida)
   - Lista de errores críticos
   - Lista de advertencias
   - Estadísticas calculadas

2. **Configuración Actual**
   - Grupos por grado (lectura)
   - Parámetros de horario (lectura)

3. **Modo Edición**
   - Grid de grupos por grado
   - Campos numéricos para parámetros
   - Validación de rangos (min/max)
   - Total de grupos calculado dinámicamente

## 🏗️ Arquitectura

### Backend
```
app/
├── models.py                  # ✅ ConfiguracionColegio ampliada
├── config_store.py           # 🆕 Store de configuración global
├── routes/
│   └── configuracion.py      # 🆕 Endpoints de configuración
└── main.py                    # ✅ Ruta incluida
```

### Frontend
```
src/app/
├── components/
│   └── configuracion/         # 🆕 Componente completo
│       ├── configuracion.component.ts
│       ├── configuracion.component.html
│       └── configuracion.component.scss
├── models/
│   └── docente.model.ts       # ✅ ConfiguracionColegio interface
├── services/
│   └── api.service.ts         # ✅ Métodos de configuración
└── app.routes.ts              # ✅ Ruta /configuracion
```

## 🎨 Interfaz de Usuario

### Diseño
- **Color principal**: Naranja (#ff9800)
- **Tarjetas organizadas** por secciones
- **Grid responsive** para grupos
- **Badges visuales** para tipos de grado
- **Alertas contextuales** de validación

### Funcionalidades UX
- Modo lectura/edición separados
- Confirmación antes de resetear
- Deshabilitación de botones durante guardado
- Feedback visual de estado
- Alertas informativas sobre impacto

## ⚠️ Consideraciones Importantes

1. **Impacto en Asignaciones**
   - Al modificar la configuración, se limpian TODAS las asignaciones
   - Debe ejecutarse la optimización nuevamente
   - Los docentes mantienen sus horas en 0

2. **Regeneración de Grupos**
   - Los grupos se regeneran según los nuevos números
   - Los IDs pueden cambiar

3. **Validaciones**
   - Los valores deben ser positivos
   - Se calculan automáticamente las necesidades
   - Se muestran advertencias si faltan docentes

## 🚀 Flujo de Uso

1. Usuario accede a **⚙️ Configuración**
2. Ve el estado actual y validación
3. Click en **✏️ Editar Configuración**
4. Modifica parámetros necesarios
5. Click en **💾 Guardar Cambios**
6. Sistema limpia asignaciones y regenera grupos
7. Usuario debe ir a **🚀 Optimización** para ejecutar nuevo cálculo

## 📝 Ejemplo de Uso

```typescript
// Frontend - Obtener configuración
this.apiService.getConfiguracion().subscribe(config => {
  console.log('Grupos totales:', Object.values(config.grupos_por_grado)
    .reduce((sum, val) => sum + val, 0));
});

// Frontend - Actualizar configuración
const nuevaConfig = {
  ...configActual,
  horas_maximas_docente: 22,
  grupos_por_grado: {
    ...configActual.grupos_por_grado,
    'Séptimo': 12  // Aumentar de 10 a 12
  }
};

this.apiService.updateConfiguracion(nuevaConfig).subscribe(() => {
  console.log('Configuración actualizada');
});
```

## ✨ Beneficios

1. **Flexibilidad**: Ajustar parámetros sin código
2. **Proyecciones**: Probar diferentes escenarios
3. **Validación**: Advertencias automáticas
4. **Seguridad**: Validación de rangos
5. **Usabilidad**: Interfaz intuitiva

## 🔮 Posibles Mejoras Futuras

- [ ] Guardar historial de configuraciones
- [ ] Exportar/importar configuraciones
- [ ] Comparar escenarios
- [ ] Simulación sin aplicar cambios
- [ ] Configuraciones por año escolar
- [ ] Backup automático antes de cambios

---

**¡La configuración ahora es completamente dinámica! 🎉**
