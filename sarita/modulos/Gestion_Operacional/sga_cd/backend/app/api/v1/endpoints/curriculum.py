from typing import List, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()

# --- PlanCurricular Endpoints ---

@router.get("/planes/", response_model=List[schemas.PlanCurricular])
def read_planes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve curriculum plans for the current tenant.
    """
    tenant_id = 1 # Placeholder for current_user.inquilino_id
    planes = crud.curriculum.get_planes_by_tenant(db, inquilino_id=tenant_id, skip=skip, limit=limit)
    return planes

@router.post("/planes/", response_model=schemas.PlanCurricular)
def create_plan(
    *,
    db: Session = Depends(deps.get_db),
    plan_in: schemas.PlanCurricularCreate,
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Create a new curriculum plan.
    """
    plan = crud.curriculum.create_plan(db=db, obj_in=plan_in)
    return plan

# --- PlanCurricularTema Endpoints ---

@router.post("/temas/", response_model=schemas.PlanCurricularTema)
def create_tema(
    *,
    db: Session = Depends(deps.get_db),
    tema_in: schemas.PlanCurricularTemaCreate,
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Create a new topic for a curriculum plan.
    """
    tema = crud.curriculum.create_tema(db=db, obj_in=tema_in)
    return tema
