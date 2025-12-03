# 🚀 Guía de Despliegue Gratuito

Esta guía te muestra cómo desplegar LaborDoc **completamente gratis** en diferentes plataformas.

## 🏆 Mejor Opción: Render.com

### Por qué Render:
- ✅ **100% Gratis** para proyectos pequeños
- ✅ **Backend + Frontend** en una plataforma
- ✅ **Deploy automático** desde Git
- ✅ **SSL/HTTPS** incluido
- ✅ **PostgreSQL** gratis (cuando lo necesites)
- ⚠️ Se duerme después de 15 min sin uso (tarda 30s en despertar)

### Setup en 5 Pasos:

1. **Crear cuenta** en [render.com](https://render.com)

2. **Conectar GitHub:**
   - Dashboard → "New +" → "Blueprint"
   - Conectar repo `devpfan/LaborDoc`
   - Render detecta automáticamente `render.yaml`

3. **Configurar servicios:**
   - Backend: `labordoc-backend` (Web Service)
   - Frontend: `labordoc-frontend` (Static Site)

4. **Deploy automático:**
   - Push a `main` → Producción
   - Push a `develop` → Desarrollo

5. **Acceder:**
   - Backend: `https://labordoc-backend.onrender.com/api`
   - Frontend: `https://labordoc-frontend.onrender.com`
   - Docs API: `https://labordoc-backend.onrender.com/docs`

### Configuración del Backend en Render:

Si no usas `render.yaml`, configura manualmente:

```
Name: labordoc-backend
Environment: Python 3
Region: Oregon (US West)
Branch: main
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Plan: Free
```

### Configuración del Frontend en Render:

```
Name: labordoc-frontend
Environment: Static Site
Region: Oregon (US West)
Branch: main
Root Directory: frontend
Build Command: npm install && npm run build -- --configuration production
Publish Directory: dist/gestor-labor-docente-frontend
```

**IMPORTANTE**: Agregar variable de entorno en frontend:
```
API_URL = https://labordoc-backend.onrender.com/api
```

---

## 🎯 Alternativa: Railway.app

### Por qué Railway:
- ✅ **$5 crédito/mes** gratis (suficiente para este proyecto)
- ✅ **Detección automática** de servicios
- ✅ **PostgreSQL incluido**
- ✅ **No se duerme**
- ✅ **Más rápido** que Render

### Setup Railway:

1. **Crear cuenta** en [railway.app](https://railway.app)

2. **New Project** → "Deploy from GitHub repo"

3. **Seleccionar** `devpfan/LaborDoc`

4. **Railway detecta automáticamente:**
   - Backend (por `backend/requirements.txt`)
   - Frontend (por `frontend/package.json`)

5. **Configurar variables:**
   - Backend: Auto-configurado
   - Frontend: Agregar `API_URL` apuntando al backend

6. **URLs generadas:**
   - `labordoc-backend.up.railway.app`
   - `labordoc-frontend.up.railway.app`

---

## 💡 Opción Híbrida (100% Gratis Forever)

### Backend: PythonAnywhere
**Gratis para siempre, sin limitaciones de sleep**

1. Crear cuenta en [pythonanywhere.com](https://www.pythonanywhere.com)
2. Web → Add a new web app
3. Python 3.12 → Manual configuration
4. Subir código:
   ```bash
   git clone https://github.com/devpfan/LaborDoc.git
   cd LaborDoc/backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
5. Configurar WSGI file
6. URL: `tunombre.pythonanywhere.com/api`

### Frontend: Vercel
**Gratis ilimitado, CDN global**

```bash
cd frontend
npm install -g vercel
vercel login
vercel --prod
```

- URL: `labordoc.vercel.app`
- Deploy automático en cada push a `main`

---

## 🐳 Opción Docker: Fly.io

### Incluye:
- 3 apps gratis (256MB RAM c/u)
- PostgreSQL gratis (1GB)
- No se duerme

### Setup:

```bash
# Instalar CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Backend
cd backend
fly launch --name labordoc-backend --region mia
fly deploy

# Frontend  
cd ../frontend
fly launch --name labordoc-frontend --region mia
fly deploy
```

---

## 📊 Comparativa Rápida

| Plataforma | Backend | Frontend | BD | Sleep | Limitación |
|------------|---------|----------|----|----|------------|
| **Render** | ✅ | ✅ | ✅ | Sí (15min) | 750h/mes |
| **Railway** | ✅ | ✅ | ✅ | No | $5 crédito/mes |
| **Fly.io** | ✅ | ✅ | ✅ | No | 3 apps max |
| **Vercel** | ❌ | ✅ | ❌ | No | Solo frontend |
| **Netlify** | ❌ | ✅ | ❌ | No | Solo frontend |
| **PythonAnywhere** | ✅ | ❌ | ✅ | No | 1 app, lento |

---

## ✨ Mi Recomendación

### Para este proyecto (LaborDoc):

**🥇 Primera opción: Render**
- Más fácil de configurar
- Todo en un lugar
- `render.yaml` ya incluido en el repo

**🥈 Segunda opción: Railway**
- Más rápido
- No se duerme
- Mejor UX

**🥉 Tercera opción: Híbrido**
- PythonAnywhere (backend) + Vercel (frontend)
- 100% gratis forever
- Requiere más configuración

---

## 🔧 Configuración Necesaria

### Para Render/Railway:

Actualizar `frontend/src/environments/environment.prod.ts`:

```typescript
export const environment = {
  production: true,
  apiUrl: 'https://labordoc-backend.onrender.com/api'  // Cambiar según tu URL
};
```

### Para CORS en Backend:

Ya está configurado en `backend/app/main.py`, pero verifica:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "https://labordoc-frontend.onrender.com",  # Agregar tu URL
        "https://labordoc.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🚀 Deploy Inmediato

### Render (Recomendado):

1. Ve a [render.com/deploy](https://render.com/deploy)
2. Conecta GitHub
3. Selecciona repo `devpfan/LaborDoc`
4. ✅ Deploy automático en 5 minutos

### Railway (Alternativa):

1. Ve a [railway.app/new](https://railway.app/new)
2. "Deploy from GitHub repo"
3. Selecciona `devpfan/LaborDoc`
4. ✅ Deploy automático en 3 minutos

---

## 📝 Después del Deploy

1. **Obtener URLs** de backend y frontend
2. **Actualizar CORS** en `backend/app/main.py`
3. **Actualizar API_URL** en `frontend/src/environments/`
4. **Commit y push** cambios
5. **Deploy automático** se ejecuta

---

## 🆘 Troubleshooting

### Backend no inicia:
```bash
# Verificar logs en Render/Railway
# Asegurarse que requirements.txt está en backend/
# Verificar que el comando es: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Frontend no encuentra API:
```bash
# Verificar que environment.prod.ts tiene la URL correcta
# Verificar CORS en backend
# Verificar que backend está corriendo
```

### App se duerme (Render):
```bash
# Soluciones:
# 1. Upgrade a plan de pago ($7/mes)
# 2. Usar Railway (no se duerme)
# 3. Usar cron job para hacer ping cada 10 min
```

---

**¡Tu proyecto estará online en menos de 10 minutos! 🎉**
