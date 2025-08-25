from typing import Generator, Any, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.schemas.token import TokenData
from app import crud
from models import user as user_model


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token"
)

def get_db() -> Generator:
    """
    Dependency to get a DB session for each request.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> user_model.Usuario:
    """
    Dependency to get the current user from the token.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenData(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    # The 'sub' field in the token should contain the user ID.
    user = db.query(user_model.Usuario).filter(user_model.Usuario.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_active_user(
    current_user: user_model.Usuario = Depends(get_current_user),
) -> user_model.Usuario:
    """
    Dependency to get the current active user.
    Raises an exception if the user is inactive.
    """
    if not current_user.activo:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def RoleRequired(required_roles: List[str]):
    """
    A dependency factory that returns a dependency to check for required roles.
    """
    class RoleChecker:
        def __init__(self, required_roles: List[str]):
            self.required_roles = required_roles

        def __call__(self, user: user_model.Usuario = Depends(get_current_active_user)):
            if user.rol not in self.required_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"User role '{user.rol}' is not authorized. Requires one of: {self.required_roles}.",
                )
            return user
    return RoleChecker(required_roles)
