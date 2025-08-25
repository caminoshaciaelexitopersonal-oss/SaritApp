from sqlalchemy.orm import Session
from typing import List

from models.academic import Escenario, EscenarioParte, Reserva
from app.schemas.escenario import EscenarioCreate, EscenarioUpdate, ReservaCreate, ReservaUpdate

# --- CRUD for Escenario ---

def get_escenario(db: Session, escenario_id: int) -> Escenario | None:
    return db.query(Escenario).filter(Escenario.id == escenario_id).first()

def get_escenarios_by_tenant(
    db: Session, *, inquilino_id: int, skip: int = 0, limit: int = 100
) -> List[Escenario]:
    return (
        db.query(Escenario)
        .filter(Escenario.inquilino_id == inquilino_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_escenario(db: Session, *, obj_in: EscenarioCreate) -> Escenario:
    db_obj = Escenario(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# --- CRUD for Reserva ---

def get_reservas_by_escenario_parte(
    db: Session, *, escenario_parte_id: int, skip: int = 0, limit: int = 100
) -> List[Reserva]:
    return (
        db.query(Reserva)
        .filter(Reserva.escenario_parte_id == escenario_parte_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_reserva(db: Session, *, obj_in: ReservaCreate) -> Reserva:
    db_obj = Reserva(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
