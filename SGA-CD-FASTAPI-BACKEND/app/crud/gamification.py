from sqlalchemy.orm import Session
from typing import List

from models.gamification import (
    GamificacionAccion, GamificacionPuntosLog, GamificacionMedalla, GamificacionMedallaObtenida
)
from app.schemas.gamification import (
    GamificacionAccionCreate, GamificacionPuntosLogCreate, GamificacionMedallaCreate
)

# --- CRUD for GamificacionAccion ---

def get_accion(db: Session, accion_id: int) -> GamificacionAccion | None:
    return db.query(GamificacionAccion).filter(GamificacionAccion.id == accion_id).first()

def get_acciones_by_tenant(
    db: Session, *, inquilino_id: int, skip: int = 0, limit: int = 100
) -> List[GamificacionAccion]:
    return (
        db.query(GamificacionAccion)
        .filter(GamificacionAccion.inquilino_id == inquilino_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_accion(db: Session, *, obj_in: GamificacionAccionCreate) -> GamificacionAccion:
    db_obj = GamificacionAccion(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# --- CRUD for GamificacionPuntosLog ---

def create_puntos_log(db: Session, *, obj_in: GamificacionPuntosLogCreate) -> GamificacionPuntosLog:
    db_obj = GamificacionPuntosLog(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# --- CRUD for GamificacionMedalla ---

def get_medalla(db: Session, medalla_id: int) -> GamificacionMedalla | None:
    return db.query(GamificacionMedalla).filter(GamificacionMedalla.id == medalla_id).first()

def create_medalla(db: Session, *, obj_in: GamificacionMedallaCreate) -> GamificacionMedalla:
    db_obj = GamificacionMedalla(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# ... and so on for other gamification models as needed.
