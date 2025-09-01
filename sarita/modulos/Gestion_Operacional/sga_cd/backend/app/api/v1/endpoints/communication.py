from typing import List, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()

# --- Chat Endpoints ---

@router.post("/chat/conversaciones/", response_model=schemas.ChatConversacion)
def create_conversacion(
    *,
    db: Session = Depends(deps.get_db),
    conv_in: schemas.ChatConversacionCreate,
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Create a new chat conversation.
    """
    conversacion = crud.communication.create_conversacion(db=db, obj_in=conv_in)
    return conversacion

@router.post("/chat/mensajes/", response_model=schemas.ChatMensaje)
def create_mensaje(
    *,
    db: Session = Depends(deps.get_db),
    msg_in: schemas.ChatMensajeCreate,
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Post a new message in a conversation.
    """
    # TODO: Add security check to ensure user is a participant of the conversation
    mensaje = crud.communication.create_mensaje(db=db, obj_in=msg_in)
    return mensaje

# --- Foro Endpoints ---

@router.post("/foros/", response_model=schemas.ForoClase)
def create_foro(
    *,
    db: Session = Depends(deps.get_db),
    foro_in: schemas.ForoClaseCreate,
) -> Any:
    """
    Create a new forum for a class.
    """
    foro = crud.communication.create_foro(db=db, obj_in=foro_in)
    return foro

@router.post("/foros/hilos/", response_model=schemas.ForoHilo)
def create_hilo(
    *,
    db: Session = Depends(deps.get_db),
    hilo_in: schemas.ForoHiloCreate,
) -> Any:
    """
    Create a new thread in a forum.
    """
    hilo = crud.communication.create_hilo(db=db, obj_in=hilo_in)
    return hilo

@router.post("/foros/publicaciones/", response_model=schemas.ForoPublicacion)
def create_publicacion(
    *,
    db: Session = Depends(deps.get_db),
    publicacion_in: schemas.ForoPublicacionCreate,
) -> Any:
    """
    Create a new post in a forum thread.
    """
    publicacion = crud.communication.create_publicacion(db=db, obj_in=publicacion_in)
    return publicacion
