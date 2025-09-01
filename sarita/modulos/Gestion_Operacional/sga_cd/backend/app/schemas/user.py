from pydantic import BaseModel, EmailStr

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    nombre_completo: str | None = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str
    nombre_usuario: str
    rol: str
    inquilino_id: int

from typing import List

# Properties to return to client
class User(UserBase):
    id: int
    activo: bool
    roles: List[str] = []

    class Config:
        from_attributes = True
