from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Float
)
from sqlalchemy.orm import relationship
from .base import Base

class Suscripcion(Base):
    __tablename__ = "suscripciones"
    id = Column(Integer, primary_key=True, index=True)
    inquilino_id = Column(Integer, ForeignKey("inquilinos.id"), unique=True, nullable=False)
    plan = Column(String, nullable=False)
    fecha_inicio = Column(DateTime(timezone=True), nullable=False)
    fecha_fin = Column(DateTime(timezone=True))
    estado = Column(String, nullable=False) # 'en_prueba', 'activa', 'cancelada', 'vencida'
    stripe_customer_id = Column(String, index=True)
    stripe_subscription_id = Column(String, unique=True, index=True)

    inquilino = relationship("Inquilino")

class Factura(Base):
    __tablename__ = "facturas"
    id = Column(Integer, primary_key=True, index=True)
    suscripcion_id = Column(Integer, ForeignKey("suscripciones.id"), nullable=False)
    inquilino_id = Column(Integer, ForeignKey("inquilinos.id"), nullable=False)
    monto = Column(Float, nullable=False)
    fecha_emision = Column(DateTime(timezone=True), nullable=False)
    fecha_pago = Column(DateTime(timezone=True))
    estado = Column(String, nullable=False) # 'pendiente', 'pagada', 'fallida'
    stripe_invoice_id = Column(String, unique=True, index=True)
    pdf_url = Column(String)

    suscripcion = relationship("Suscripcion")
    inquilino = relationship("Inquilino")
