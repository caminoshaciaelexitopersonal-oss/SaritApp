from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.ProcesoFormacion])
def read_procesos(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.Usuario = Depends(deps.get_current_active_user)
) -> Any:
    """
    Retrieve procesos de formacion for the current user's tenant.
    """
    tenant_id = 1 # Placeholder for current_user.inquilino_id
    procesos = crud.clase.get_procesos_by_tenant(db, inquilino_id=tenant_id, skip=skip, limit=limit)
    return procesos

@router.post("/", response_model=schemas.ProcesoFormacion)
def create_proceso(
    *,
    db: Session = Depends(deps.get_db),
    proceso_in: schemas.ProcesoFormacionCreate,
    # current_user: models.Usuario = Depends(deps.get_current_active_user)
) -> Any:
    """
    Create new proceso de formacion.
    """
    proceso = crud.clase.create_proceso(db=db, obj_in=proceso_in)
    return proceso

@router.get("/{proceso_id}", response_model=schemas.ProcesoFormacion)
def read_proceso_by_id(
    proceso_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific proceso by id.
    """
    proceso = crud.clase.get_proceso(db=db, proceso_id=proceso_id)
    if not proceso:
        raise HTTPException(status_code=404, detail="Proceso not found")
    return proceso

@router.put("/{proceso_id}", response_model=schemas.ProcesoFormacion)
def update_proceso(
    *,
    db: Session = Depends(deps.get_db),
    proceso_id: int,
    proceso_in: schemas.ProcesoFormacionUpdate,
) -> Any:
    """
    Update a proceso.
    """
    db_proceso = crud.clase.get_proceso(db=db, proceso_id=proceso_id)
    if not db_proceso:
        raise HTTPException(status_code=404, detail="Proceso not found")
    proceso = crud.clase.update_proceso(db=db, db_obj=db_proceso, obj_in=proceso_in)
    return proceso
