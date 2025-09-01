from typing import List, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.get("/me/", response_model=List[schemas.Notificacion])
def read_my_notificaciones(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.get_current_user) # This is now a dependency
) -> Any:
    """
    Retrieve notifications for the current logged-in user.
    """
    notificaciones = crud.notificacion.get_notificaciones_by_user(
        db, usuario_id=current_user.id, skip=skip, limit=limit
    )
    return notificaciones

@router.put("/{notificacion_id}/read", response_model=schemas.Notificacion)
def mark_notification_as_read(
    notificacion_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Mark a notification as read.
    """
    db_notification = crud.notificacion.mark_as_read(db, notificacion_id=notificacion_id)
    # TODO: Add security check to ensure the notification belongs to the current user
    return db_notification
