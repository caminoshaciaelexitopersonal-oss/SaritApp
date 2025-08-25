from sqlalchemy.orm import Session
from typing import List

from models.billing import Suscripcion, Factura
from app.schemas.billing import SuscripcionCreate, SuscripcionUpdate, FacturaCreate, FacturaUpdate

# --- CRUD for Suscripcion ---

def get_suscripcion_by_tenant(db: Session, inquilino_id: int) -> Suscripcion | None:
    return db.query(Suscripcion).filter(Suscripcion.inquilino_id == inquilino_id).first()

def create_suscripcion(db: Session, *, obj_in: SuscripcionCreate) -> Suscripcion:
    db_obj = Suscripcion(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_suscripcion(db: Session, *, db_obj: Suscripcion, obj_in: SuscripcionUpdate) -> Suscripcion:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# --- CRUD for Factura ---

def get_facturas_by_tenant(
    db: Session, *, inquilino_id: int, skip: int = 0, limit: int = 100
) -> List[Factura]:
    return (
        db.query(Factura)
        .filter(Factura.inquilino_id == inquilino_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_factura(db: Session, *, obj_in: FacturaCreate) -> Factura:
    db_obj = Factura(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
