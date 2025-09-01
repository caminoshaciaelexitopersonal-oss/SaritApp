from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from models import user as user_model

router = APIRouter()

@router.get("/", response_model=List[schemas.Alumno])
def read_alumnos(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: user_model.Usuario = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve alumnos for the current user's tenant.
    Accessible by any active user of the tenant.
    """
    alumnos = crud.alumno.get_multi_by_tenant(db, inquilino_id=current_user.inquilino_id, skip=skip, limit=limit)
    return alumnos

@router.post("/", response_model=schemas.Alumno)
def create_alumno(
    *,
    db: Session = Depends(deps.get_db),
    alumno_in: schemas.AlumnoCreate,
    current_user: user_model.Usuario = Depends(deps.role_required(["admin_empresa", "profesor"])),
) -> Any:
    """
    Create a new alumno.
    Only accessible by admins and teachers.
    """
    # Ensure the new alumno is for the current user's tenant
    if alumno_in.inquilino_id != current_user.inquilino_id:
        raise HTTPException(status_code=403, detail="Cannot create alumno for another tenant.")

    alumno = crud.alumno.create(db=db, obj_in=alumno_in)
    return alumno

@router.get("/{alumno_id}", response_model=schemas.Alumno)
def read_alumno_by_id(
    alumno_id: int,
    db: Session = Depends(deps.get_db),
    current_user: user_model.Usuario = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific alumno by id.
    """
    alumno = crud.alumno.get(db=db, alumno_id=alumno_id)
    if not alumno or alumno.inquilino_id != current_user.inquilino_id:
        raise HTTPException(status_code=404, detail="Alumno not found")
    return alumno

@router.put("/{alumno_id}", response_model=schemas.Alumno)
def update_alumno(
    *,
    db: Session = Depends(deps.get_db),
    alumno_id: int,
    alumno_in: schemas.AlumnoUpdate,
    current_user: user_model.Usuario = Depends(deps.role_required(["admin_empresa", "profesor"])),
) -> Any:
    """
    Update an alumno.
    """
    db_alumno = crud.alumno.get(db=db, alumno_id=alumno_id)
    if not db_alumno or db_alumno.inquilino_id != current_user.inquilino_id:
        raise HTTPException(status_code=404, detail="Alumno not found")
    alumno = crud.alumno.update(db=db, db_obj=db_alumno, obj_in=alumno_in)
    return alumno

@router.delete("/{alumno_id}", response_model=schemas.Alumno)
def delete_alumno(
    *,
    db: Session = Depends(deps.get_db),
    alumno_id: int,
    current_user: user_model.Usuario = Depends(deps.role_required(["admin_empresa"])),
) -> Any:
    """
    Delete an alumno. (Restricted to tenant admins)
    """
    db_alumno = crud.alumno.get(db=db, alumno_id=alumno_id)
    if not db_alumno or db_alumno.inquilino_id != current_user.inquilino_id:
        raise HTTPException(status_code=404, detail="Alumno not found")
    alumno = crud.alumno.remove(db=db, id=alumno_id)
    return alumno


@router.get("/{alumno_id}/progreso", response_model=schemas.AlumnoProgreso)
def read_alumno_progreso(
    *,
    db: Session = Depends(deps.get_db),
    alumno_id: int,
    current_user: user_model.Usuario = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific alumno's progress by id.
    """
    # Here, alumno_id is the user_id of the student.
    alumno_user = crud.user.get(db=db, id=alumno_id)
    if not alumno_user or "alumno" not in alumno_user.roles:
        raise HTTPException(status_code=404, detail="Alumno not found")

    if alumno_user.inquilino_id != current_user.inquilino_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this tenant's data")

    # Permission check
    user_roles = set(current_user.roles)
    is_admin_or_profesor = user_roles.intersection({"admin_empresa", "profesor", "jefe_area", "coordinador"})
    is_parent = "padre_acudiente" in user_roles and alumno_user in current_user.hijos

    if not is_admin_or_profesor and not is_parent:
        raise HTTPException(status_code=403, detail="Not enough permissions to view student progress")

    # Mock data for now, as CRUD functions for progress are not yet implemented.
    # TODO: Replace with real data fetching from CRUD layer.
    progreso_data = {
        "asistencia_porcentaje": 85.5,
        "asistencia_status": "buena",
        "calificaciones_recientes": [
            {"materia": "Matemáticas", "nota": "A"},
            {"materia": "Deportes", "nota": "B+"},
        ],
        "logros_gamificacion": [
            {"nombre": "Madrugador"},
            {"nombre": "Participante Activo"},
        ],
    }
    return progreso_data
