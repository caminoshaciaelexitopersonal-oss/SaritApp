from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()

# --- Suscripcion Endpoints ---

@router.get("/suscripcion/", response_model=schemas.Suscripcion)
def read_suscripcion(
    db: Session = Depends(deps.get_db),
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve suscripcion for the current user's tenant.
    """
    tenant_id = 1 # Placeholder for current_user.inquilino_id
    suscripcion = crud.billing.get_suscripcion_by_tenant(db, inquilino_id=tenant_id)
    if not suscripcion:
        raise HTTPException(status_code=404, detail="Suscripcion not found")
    return suscripcion

@router.put("/suscripcion/", response_model=schemas.Suscripcion)
def update_suscripcion(
    *,
    db: Session = Depends(deps.get_db),
    suscripcion_in: schemas.SuscripcionUpdate,
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Update the subscription for the current tenant.
    (e.g., changing plan, canceling)
    """
    tenant_id = 1 # Placeholder
    db_suscripcion = crud.billing.get_suscripcion_by_tenant(db, inquilino_id=tenant_id)
    if not db_suscripcion:
        raise HTTPException(status_code=404, detail="Suscripcion not found")
    suscripcion = crud.billing.update_suscripcion(db=db, db_obj=db_suscripcion, obj_in=suscripcion_in)
    return suscripcion

# --- Factura Endpoints ---

@router.get("/facturas/", response_model=List[schemas.Factura])
def read_facturas(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve facturas for the current user's tenant.
    """
    tenant_id = 1 # Placeholder
    facturas = crud.billing.get_facturas_by_tenant(db, inquilino_id=tenant_id, skip=skip, limit=limit)
    return facturas
