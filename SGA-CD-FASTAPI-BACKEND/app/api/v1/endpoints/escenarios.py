from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()

# --- Escenario Endpoints ---

@router.get("/", response_model=List[schemas.Escenario])
def read_escenarios(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve escenarios for the current tenant.
    """
    tenant_id = 1 # Placeholder for current_user.inquilino_id
    escenarios = crud.escenario.get_escenarios_by_tenant(db, inquilino_id=tenant_id, skip=skip, limit=limit)
    return escenarios

@router.post("/", response_model=schemas.Escenario)
def create_escenario(
    *,
    db: Session = Depends(deps.get_db),
    escenario_in: schemas.EscenarioCreate,
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Create new escenario.
    """
    escenario = crud.escenario.create_escenario(db=db, obj_in=escenario_in)
    return escenario

# --- Reserva Endpoints ---

@router.get("/{escenario_id}/reservas/", response_model=List[schemas.Reserva])
def read_reservas(
    escenario_id: int, # This is not quite right, should be escenario_parte_id
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve reservas for a specific escenario part.
    A more RESTful approach might be /escenario-partes/{parte_id}/reservas
    """
    # This logic needs refinement, as reservations are per 'parte' not 'escenario'
    # For now, this is a placeholder.
    # reservas = crud.escenario.get_reservas_by_escenario_parte(...)
    return []


@router.post("/reservas/", response_model=schemas.Reserva)
def create_reserva(
    *,
    db: Session = Depends(deps.get_db),
    reserva_in: schemas.ReservaCreate,
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Create a new reserva.
    """
    # TODO: Add logic to check for overlapping reservations
    reserva = crud.escenario.create_reserva(db=db, obj_in=reserva_in)
    return reserva
