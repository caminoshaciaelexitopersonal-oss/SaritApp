from typing import List, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()

# --- Inscripcion Endpoints ---

@router.get("/inscripciones/clase/{clase_id}", response_model=List[schemas.Inscripcion])
def read_inscripciones_by_clase(
    clase_id: int,
    db: Session = Depends(deps.get_db),
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve enrollments for a specific class.
    """
    # TODO: Security check to ensure user has access to this class
    inscripciones = crud.inscripcion_asistencia.get_inscripciones_by_clase(db, clase_id=clase_id)
    return inscripciones

@router.post("/inscripciones/", response_model=schemas.Inscripcion)
def create_inscripcion(
    *,
    db: Session = Depends(deps.get_db),
    inscripcion_in: schemas.InscripcionCreate,
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Create a new enrollment.
    """
    inscripcion = crud.inscripcion_asistencia.create_inscripcion(db=db, obj_in=inscripcion_in)
    return inscripcion

# --- Asistencia Endpoints ---

@router.get("/asistencias/clase/{clase_id}", response_model=List[schemas.Asistencia])
def read_asistencias_by_clase(
    clase_id: int,
    db: Session = Depends(deps.get_db),
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve attendance for a specific class.
    """
    asistencias = crud.inscripcion_asistencia.get_asistencias_by_clase(db, clase_id=clase_id)
    return asistencias

@router.post("/asistencias/", response_model=schemas.Asistencia)
def create_asistencia(
    *,
    db: Session = Depends(deps.get_db),
    asistencia_in: schemas.AsistenciaCreate,
    # current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Log attendance for a student in a class.
    """
    asistencia = crud.inscripcion_asistencia.create_asistencia(db=db, obj_in=asistencia_in)
    return asistencia
