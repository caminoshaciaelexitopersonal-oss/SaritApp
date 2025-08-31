from pydantic import BaseModel, EmailStr

class TenantCreate(BaseModel):
    nombre_empresa: str
    admin_nombre_completo: str
    admin_email: EmailStr
    admin_password: str

class Tenant(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True

class TenantAdmin(BaseModel):
    id: int
    nombre_usuario: str
    correo: EmailStr

    class Config:
        orm_mode = True

class TenantCreateResponse(BaseModel):
    tenant: Tenant
    admin: TenantAdmin
