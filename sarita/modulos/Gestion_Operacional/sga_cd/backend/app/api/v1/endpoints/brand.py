from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.schemas import brand as schemas_brand

router = APIRouter()

@router.get("/", response_model=schemas_brand.BrandProfile)
def read_brand_profile(
    db: Session = Depends(deps.get_db),
    current_user: models.user.Usuario = Depends(deps.role_required(["admin_general"]))
):
    """
    Retrieve the brand profile for the current user's tenant.
    """
    profile = crud.brand.get_brand_profile(db, inquilino_id=current_user.inquilino_id)
    if not profile:
        # If no profile exists, create a default one to ensure frontend has something to work with
        default_profile_data = schemas_brand.BrandProfileCreate()
        profile = crud.brand.create_or_update_brand_profile(
            db=db, inquilino_id=current_user.inquilino_id, obj_in=default_profile_data
        )
    return profile

@router.post("/", response_model=schemas_brand.BrandProfile)
def create_or_update_brand_profile(
    *,
    db: Session = Depends(deps.get_db),
    profile_in: schemas_brand.BrandProfileCreate,
    current_user: models.user.Usuario = Depends(deps.role_required(["admin_general"]))
):
    """
    Create or update the brand profile for the current user's tenant.
    """
    profile = crud.brand.create_or_update_brand_profile(
        db=db, inquilino_id=current_user.inquilino_id, obj_in=profile_in
    )
    return profile
