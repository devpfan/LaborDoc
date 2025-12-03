# 🔄 Workflow de Desarrollo

## Estrategia de Ramas

```
develop (local) ──► tests automáticos ──► merge ──► main ──► 🚀 PRODUCCIÓN
```

## 📋 Proceso Recomendado

### 1. Desarrollo Local (rama `develop`)

```bash
# Trabajar en develop
git checkout develop

# Iniciar servidores locales
./start.sh
# o manualmente:
# Terminal 1: cd backend && source venv/bin/activate && uvicorn app.main:app --reload
# Terminal 2: cd frontend && npm start

# Hacer cambios...
# Probar en: http://localhost:4200
```

### 2. Commit y Push a Develop

```bash
# Agregar cambios
git add .
git commit -m "feat: descripción del cambio"

# Push a develop
git push origin develop
```

**✅ GitHub Actions ejecutará automáticamente:**
- Instalación de dependencias
- Build del frontend
- Validación de que todo compila
- Tests (cuando los agregues)

### 3. Merge a Main (Producción)

Cuando todo esté probado y listo:

```bash
# Cambiar a main
git checkout main

# Traer últimos cambios
git pull origin main

# Merge desde develop
git merge develop

# Push a main (dispara deploy automático)
git push origin main
```

**🚀 GitHub Actions + Render/Railway:**
- Build de producción
- Deploy automático
- La app estará live en minutos

## 🎯 Ventajas de este Workflow

✅ **Develop = tu ambiente local**
- No pagas por servidor de desarrollo
- Cambios instantáneos
- Debugging fácil

✅ **Main = producción única**
- Deploy automático
- Solo una instancia a mantener
- Gratis en Render/Railway

✅ **Tests automáticos**
- Cada push a develop valida el código
- No mergeas código roto a main
- Confianza antes del deploy

## 📊 Estados de las Ramas

### Rama `develop`
- **Propósito**: Desarrollo activo
- **Ambiente**: Local (localhost)
- **Cuando pusheas**: Se ejecutan tests
- **No despliega** a ningún servidor

### Rama `main`
- **Propósito**: Producción
- **Ambiente**: Render/Railway (público)
- **Cuando pusheas**: Deploy automático
- **URL**: Tu dominio de producción

## 🔧 Comandos Rápidos

```bash
# Ver en qué rama estás
git branch

# Cambiar a develop
git checkout develop

# Cambiar a main
git checkout main

# Ver diferencias entre ramas
git diff main..develop

# Ver commits en develop que no están en main
git log main..develop --oneline

# Ver estado de GitHub Actions
# Ve a: https://github.com/devpfan/LaborDoc/actions
```

## 🆘 Si algo sale mal en producción

### Rollback rápido:

```bash
# Ver commits recientes
git log --oneline -5

# Revertir al commit anterior
git checkout main
git revert HEAD
git push origin main
# ✅ Deploy automático del rollback
```

### Hotfix urgente:

```bash
# Crear rama de hotfix desde main
git checkout main
git checkout -b hotfix/fix-urgente

# Hacer el fix
# ... editar archivos ...

# Commit
git add .
git commit -m "fix: arreglo urgente"

# Merge directo a main
git checkout main
git merge hotfix/fix-urgente
git push origin main  # 🚀 Deploy inmediato

# También merge a develop para mantener sincronizado
git checkout develop
git merge hotfix/fix-urgente
git push origin develop
```

## 📝 Buenas Prácticas

### Commits semánticos:

```bash
git commit -m "feat: agregar nueva funcionalidad"     # Nueva feature
git commit -m "fix: corregir bug en optimización"     # Bug fix
git commit -m "docs: actualizar README"               # Documentación
git commit -m "style: formatear código"               # Formato
git commit -m "refactor: reorganizar componentes"     # Refactoring
git commit -m "test: agregar tests unitarios"         # Tests
git commit -m "chore: actualizar dependencias"        # Mantenimiento
```

### Antes de merge a main:

```bash
# ✅ Checklist:
# [ ] Probado en local (http://localhost:4200)
# [ ] Tests pasan en develop (revisar GitHub Actions)
# [ ] Frontend compila sin errores (npm run build)
# [ ] Backend funciona sin errores
# [ ] Sin console.log o código de debug
# [ ] Commit messages claros
```

## 🎨 Flujo Visual

```
┌─────────────────────────────────────────────────────────────┐
│  DESARROLLO LOCAL (develop)                                 │
│  ┌────────────┐                                            │
│  │ Hacer      │ → git commit → git push origin develop    │
│  │ cambios    │                      ↓                     │
│  └────────────┘              GitHub Actions               │
│       ↓                       (tests + build)              │
│  http://localhost:4200              ↓                      │
│  http://localhost:8000           ✅ PASS                   │
└─────────────────────────────────────────────────────────────┘
                                   ↓
                          ¿Todo funciona bien?
                                   ↓
┌─────────────────────────────────────────────────────────────┐
│  PRODUCCIÓN (main)                                          │
│  git merge develop → git push origin main                  │
│                            ↓                                │
│                    GitHub Actions                           │
│                    (build + deploy)                         │
│                            ↓                                │
│              Render/Railway (auto-deploy)                   │
│                            ↓                                │
│         🌐 https://tu-app.onrender.com                     │
└─────────────────────────────────────────────────────────────┘
```

## 🔗 Links Útiles

- **Repo**: https://github.com/devpfan/LaborDoc
- **Actions**: https://github.com/devpfan/LaborDoc/actions
- **Render**: https://dashboard.render.com (después de conectar)
- **Railway**: https://railway.app/dashboard (después de conectar)

---

**¡Workflow simple y efectivo! 🚀**
