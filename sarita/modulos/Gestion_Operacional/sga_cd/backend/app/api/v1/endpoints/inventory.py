from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()

# --- Elemento Endpoints ---

@router.get("/elementos/", response_model=List[schemas.Elemento])
def read_elementos(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve elementos for the current tenant.
    """
    tenant_id = 1 # Placeholder for current_user.inquilino_id
    elementos = crud.inventory.get_elementos_by_tenant(db, inquilino_id=tenant_id, skip=skip, limit=limit)
    return elementos

@router.post("/elementos/", response_model=schemas.Elemento)
def create_elemento(
    *,
    db: Session = Depends(deps.get_db),
    elemento_in: schemas.ElementoCreate,
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Create new elemento.
    """
    elemento = crud.inventory.create_elemento(db=db, obj_in=elemento_in)
    return elemento

# --- Prestamo Endpoints ---

@router.get("/prestamos/", response_model=List[schemas.Prestamo])
def read_prestamos(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve prestamos for the current tenant.
    """
    tenant_id = 1 # Placeholder for current_user.inquilino_id
    prestamos = crud.inventory.get_prestamos_by_tenant(db, inquilino_id=tenant_id, skip=skip, limit=limit)
    return prestamos

@router.post("/prestamos/", response_model=schemas.Prestamo)
def create_prestamo(
    *,
    db: Session = Depends(deps.get_db),
    prestamo_in: schemas.PrestamoCreate,
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Create new prestamo.
    """
    prestamo = crud.inventory.create_prestamo(db=db, obj_in=prestamo_in)
    return prestamo
