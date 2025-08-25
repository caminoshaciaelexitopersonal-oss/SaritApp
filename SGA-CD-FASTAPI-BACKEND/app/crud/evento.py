from sqlalchemy.orm import Session
from typing import List

from models.academic import Evento, EventoParticipante
from app.schemas.evento import EventoCreate, EventoUpdate, EventoParticipanteCreate

# --- CRUD for Evento ---

def get_evento(db: Session, evento_id: int) -> Evento | None:
    return db.query(Evento).filter(Evento.id == evento_id).first()

def get_eventos_by_tenant(
    db: Session, *, inquilino_id: int, skip: int = 0, limit: int = 100
) -> List[Evento]:
    return (
        db.query(Evento)
        .filter(Evento.inquilino_id == inquilino_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_evento(db: Session, *, obj_in: EventoCreate) -> Evento:
    db_obj = Evento(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# --- CRUD for EventoParticipante ---

def add_participante_to_evento(db: Session, *, obj_in: EventoParticipanteCreate) -> EventoParticipante:
    db_obj = EventoParticipante(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
