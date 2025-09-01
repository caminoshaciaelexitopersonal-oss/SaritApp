from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import text
from jose import jwt, JWTError
from pydantic import ValidationError

from app import crud, schemas
from models import user as user_models
from app.api import deps
from app.core import security
from app.core.config import settings

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token and refresh token.
    """
    user = crud.user.get_user_by_username(db, username=form_data.username)
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.activo:
        raise HTTPException(status_code=400, detail="Inactive user")

    # El objeto user de crud.get_user_by_username ya trae los roles
    access_token_data = {
        "sub": str(user.id),
        "roles": user.roles,
        "inquilino_id": user.inquilino_id,
        "nombre_completo": user.nombre_completo
    }
    # Refresh token solo necesita el user_id
    refresh_token_data = {"sub": str(user.id)}

    return {
        "access_token": security.create_access_token(data=access_token_data),
        "refresh_token": security.create_refresh_token(data=refresh_token_data),
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=schemas.Token)
def refresh_token(
    db: Session = Depends(deps.get_db), refresh_token: str = Body(..., embed=True)
) -> Any:
    """
    OAuth2 compatible token refresh.
    """
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type, expected 'refresh'",
            )
        token_data = schemas.TokenData(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(user_models.Usuario).filter(user_models.Usuario.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.activo:
        raise HTTPException(status_code=400, detail="Inactive user")

    # Como el objeto de la query no trae roles, los buscamos manualmente
    query = text("SELECT r.nombre FROM roles r JOIN user_roles ur ON r.id = ur.role_id WHERE ur.user_id = :user_id")
    roles_result = db.execute(query, {"user_id": user.id}).fetchall()
    user_roles = [row[0] for row in roles_result]

    access_token_data = {
        "sub": str(user.id),
        "roles": user_roles,
        "inquilino_id": user.inquilino_id,
        "nombre_completo": user.nombre_completo,
    }

    return {
        "access_token": security.create_access_token(data=access_token_data),
        "refresh_token": refresh_token,  # devolvemos el mismo refresh token
        "token_type": "bearer",
    }


@router.post("/register", response_model=schemas.User)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_user_by_username(db, username=user_in.nombre_usuario)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create_user(db, user=user_in)
    return user