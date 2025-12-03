from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Docente
from app.database import db

router = APIRouter()

@router.get("/", response_model=List[Docente])
def listar_docentes():
    """Obtiene la lista de todos los docentes"""
    return db.obtener_docentes()

@router.get("/{docente_id}", response_model=Docente)
def obtener_docente(docente_id: int):
    """Obtiene un docente por ID"""
    docente = db.obtener_docente(docente_id)
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    return docente

@router.post("/", response_model=Docente)
def crear_docente(docente: Docente):
    """Crea un nuevo docente"""
    return db.agregar_docente(docente)

@router.put("/{docente_id}", response_model=Docente)
def actualizar_docente(docente_id: int, docente: Docente):
    """Actualiza un docente existente"""
    docente_actualizado = db.actualizar_docente(docente_id, docente)
    if not docente_actualizado:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    return docente_actualizado

@router.delete("/{docente_id}")
def eliminar_docente(docente_id: int):
    """Elimina un docente"""
    if not db.eliminar_docente(docente_id):
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    return {"mensaje": "Docente eliminado correctamente"}

@router.get("/{docente_id}/asignaciones")
def obtener_asignaciones_docente(docente_id: int):
    """Obtiene todas las asignaciones de un docente"""
    docente = db.obtener_docente(docente_id)
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    
    asignaciones = db.obtener_asignaciones_docente(docente_id)
    return {
        "docente": docente,
        "asignaciones": asignaciones,
        "total_horas": sum([a.horas_semanales for a in asignaciones])
    }
