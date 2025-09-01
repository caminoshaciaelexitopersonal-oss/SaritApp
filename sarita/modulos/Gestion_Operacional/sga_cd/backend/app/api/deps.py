from typing import Generator, Any, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.schemas.token import TokenData
from app import crud
from models import user as user_model


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"  # Updated to new login URL
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

def get_token_data(token: str = Depends(reusable_oauth2)) -> TokenData:
    """
    Dependency that decodes and validates the JWT token, returning the payload.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token type, expected 'access'",
            )
        token_data = TokenData(
            sub=payload.get("sub"),
            roles=payload.get("roles", []),
            inquilino_id=payload.get("inquilino_id")
        )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return token_data


def get_current_user(
    db: Session = Depends(get_db), token_data: TokenData = Depends(get_token_data)
) -> user_model.Usuario:
    """
    Dependency to get the current user from the token payload.
    """
    user = db.query(user_model.Usuario).filter(user_model.Usuario.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Attach roles from token for convenience in other dependencies or endpoints
    user.roles = token_data.roles
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


def role_required(required_roles: List[str]):
    """
    A dependency factory that returns a dependency to check for required roles.
    This version checks the roles present in the JWT token payload,
    avoiding an extra DB call.
    """
    def role_checker(token_data: TokenData = Depends(get_token_data)) -> None:
        user_roles = set(token_data.roles)
        if not user_roles.intersection(set(required_roles)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not authorized. Requires one of the following roles: {required_roles}",
            )
        return token_data

    return role_checker