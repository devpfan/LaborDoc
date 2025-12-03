from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Grupo
from app.database import db

router = APIRouter()

@router.get("/", response_model=List[Grupo])
def listar_grupos():
    """Obtiene la lista de todos los grupos"""
    return db.obtener_grupos()

@router.get("/{grupo_id}", response_model=Grupo)
def obtener_grupo(grupo_id: int):
    """Obtiene un grupo por ID"""
    grupo = db.obtener_grupo(grupo_id)
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return grupo

@router.get("/grado/{grado}")
def obtener_grupos_por_grado(grado: str):
    """Obtiene todos los grupos de un grado específico"""
    grupos = db.obtener_grupos_por_grado(grado)
    return grupos

@router.post("/", response_model=Grupo)
def crear_grupo(grupo: Grupo):
    """Crea un nuevo grupo"""
    return db.agregar_grupo(grupo)
