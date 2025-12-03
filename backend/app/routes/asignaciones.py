from fastapi import APIRouter
from typing import List
from app.models import Asignacion
from app.database import db

router = APIRouter()

@router.get("/", response_model=List[Asignacion])
def listar_asignaciones():
    """Obtiene todas las asignaciones"""
    return db.obtener_asignaciones()

@router.post("/limpiar")
def limpiar_asignaciones():
    """Limpia todas las asignaciones y resetea los docentes"""
    db.limpiar_asignaciones()
    return {"mensaje": "Asignaciones limpiadas correctamente"}
