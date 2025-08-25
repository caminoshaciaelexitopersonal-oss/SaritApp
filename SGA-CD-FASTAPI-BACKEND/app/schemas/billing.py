from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- Suscripcion Schemas ---

class SuscripcionBase(BaseModel):
    plan: str
    estado: str
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None

class SuscripcionCreate(SuscripcionBase):
    inquilino_id: int

class SuscripcionUpdate(BaseModel):
    # Only some fields should be updatable
    plan: Optional[str] = None
    estado: Optional[str] = None
    fecha_fin: Optional[datetime] = None

class SuscripcionInDBBase(SuscripcionBase):
    id: int
    inquilino_id: int
    class Config:
        from_attributes = True

class Suscripcion(SuscripcionInDBBase):
    pass


# --- Factura Schemas ---

class FacturaBase(BaseModel):
    monto: float
    estado: str
    fecha_emision: datetime
    fecha_pago: Optional[datetime] = None
    stripe_invoice_id: Optional[str] = None
    pdf_url: Optional[str] = None

class FacturaCreate(FacturaBase):
    inquilino_id: int
    suscripcion_id: int

class FacturaUpdate(BaseModel):
    estado: Optional[str] = None
    fecha_pago: Optional[datetime] = None
    pdf_url: Optional[str] = None

class FacturaInDBBase(FacturaBase):
    id: int
    suscripcion_id: int
    inquilino_id: int
    class Config:
        from_attributes = True

class Factura(FacturaInDBBase):
    pass
