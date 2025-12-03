from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import docentes, grupos, asignaciones, optimizacion, configuracion

app = FastAPI(
    title="Gestor de Labor Docente",
    description="Sistema de gestión y optimización de asignación docente por niveles",
    version="1.0.0"
)

# Configuración CORS para Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(docentes.router, prefix="/api/docentes", tags=["Docentes"])
app.include_router(grupos.router, prefix="/api/grupos", tags=["Grupos"])
app.include_router(asignaciones.router, prefix="/api/asignaciones", tags=["Asignaciones"])
app.include_router(optimizacion.router, prefix="/api/optimizacion", tags=["Optimización"])
app.include_router(configuracion.router, prefix="/api/configuracion", tags=["Configuración"])

@app.get("/")
def root():
    return {
        "mensaje": "API Gestor de Labor Docente",
        "version": "1.0.0",
        "documentacion": "/docs"
    }
