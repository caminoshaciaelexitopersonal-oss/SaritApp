from sqlalchemy.orm import Session
from models import brand as models
from app.schemas import brand as schemas # This schema will be created later

def get_brand_profile(db: Session, inquilino_id: int) -> models.BrandProfile | None:
    """
    Retrieves the brand profile for a given tenant.
    """
    return db.query(models.BrandProfile).filter(models.BrandProfile.inquilino_id == inquilino_id).first()

def create_or_update_brand_profile(
    db: Session, *, inquilino_id: int, obj_in: schemas.BrandProfileCreate
) -> models.BrandProfile:
    """
    Creates a new brand profile or updates an existing one for a given tenant.
    """
    db_obj = get_brand_profile(db, inquilino_id=inquilino_id)

    if db_obj:
        # Update existing object
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
    else:
        # Create new object
        db_obj = models.BrandProfile(**obj_in.model_dump(), inquilino_id=inquilino_id)
        db.add(db_obj)

    db.commit()
    db.refresh(db_obj)
    return db_obj
