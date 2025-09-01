from typing import List, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Evento])
def read_eventos(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve eventos for the current tenant.
    """
    tenant_id = 1 # Placeholder for current_user.inquilino_id
    eventos = crud.evento.get_eventos_by_tenant(db, inquilino_id=tenant_id, skip=skip, limit=limit)
    return eventos

@router.post("/", response_model=schemas.Evento)
def create_evento(
    *,
    db: Session = Depends(deps.get_db),
    evento_in: schemas.EventoCreate,
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Create new evento.
    """
    evento = crud.evento.create_evento(db=db, obj_in=evento_in)
    return evento

@router.post("/participantes/", response_model=schemas.EventoParticipante)
def add_participante_to_evento(
    *,
    db: Session = Depends(deps.get_db),
    participante_in: schemas.EventoParticipanteCreate,
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Add a participant to an event.
    """
    # TODO: Security check to ensure event and user belong to the same tenant
    participante = crud.evento.add_participante_to_evento(db=db, obj_in=participante_in)
    return participante
