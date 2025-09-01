from sqlalchemy.orm import Session
from typing import List, Any
from fastapi.encoders import jsonable_encoder

from models import calendar as models
from app.schemas import scheduled_post as schemas

def get(db: Session, id: Any) -> models.ScheduledPost | None:
    return db.query(models.ScheduledPost).filter(models.ScheduledPost.id == id).first()

def get_multi_by_tenant(
    db: Session, *, inquilino_id: int, skip: int = 0, limit: int = 100
) -> List[models.ScheduledPost]:
    return (
        db.query(models.ScheduledPost)
        .filter(models.ScheduledPost.inquilino_id == inquilino_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_with_tenant(
    db: Session, *, obj_in: schemas.ScheduledPostCreate, inquilino_id: int
) -> models.ScheduledPost:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = models.ScheduledPost(**obj_in_data, inquilino_id=inquilino_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session, *, db_obj: models.ScheduledPost, obj_in: schemas.ScheduledPostUpdate
) -> models.ScheduledPost:
    obj_data = jsonable_encoder(db_obj)
    update_data = obj_in.model_dump(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove(db: Session, *, id: int) -> models.ScheduledPost:
    obj = db.query(models.ScheduledPost).get(id)
    db.delete(obj)
    db.commit()
    return obj
