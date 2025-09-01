from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app import schemas
import models
from app.api import deps

router = APIRouter()

@router.get("/hijos", response_model=List[schemas.User], tags=["Padre Acudiente"])
def read_hijos(
    db: Session = Depends(deps.get_db),
    current_user: models.Usuario = Depends(deps.get_current_active_user),
):
    """
    Retrieve the children of the current user (padre_acudiente).
    """
    # Use the roles from the token attached by the dependency
    if "padre_acudiente" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Required role: padre_acudiente",
        )

    # The 'hijos' relationship returns a list of user models. These models do not
    # have the `roles` attribute attached, so we must fetch them manually.
    hijos_models = current_user.hijos
    hijos_schemas = []
    for hijo in hijos_models:
        # Manually fetch roles for each child to ensure compatibility with the new RBAC system
        query = text("SELECT r.nombre FROM roles r JOIN user_roles ur ON r.id = ur.role_id WHERE ur.user_id = :user_id")
        roles_result = db.execute(query, {"user_id": hijo.id}).fetchall()
        hijo_roles = [row[0] for row in roles_result]

        hijo_schema = schemas.User(
            id=hijo.id,
            email=hijo.correo,
            nombre_completo=hijo.nombre_completo,
            activo=hijo.activo,
            roles=hijo_roles # Use the manually fetched roles
        )
        hijos_schemas.append(hijo_schema)

    return hijos_schemas
