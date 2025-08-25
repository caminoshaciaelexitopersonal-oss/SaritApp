from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Boolean
)
from sqlalchemy.orm import relationship
from .base import Base

class GamificacionAccion(Base):
    __tablename__ = "gamificacion_acciones"
    id = Column(Integer, primary_key=True, index=True)
    inquilino_id = Column(Integer, ForeignKey("inquilinos.id"), nullable=False)
    accion_key = Column(String, nullable=False)
    puntos = Column(Integer, nullable=False)

class GamificacionPuntosLog(Base):
    __tablename__ = "gamificacion_puntos_log"
    id = Column(Integer, primary_key=True, index=True)
    inquilino_id = Column(Integer, ForeignKey("inquilinos.id"), nullable=False)
    alumno_id = Column(Integer, ForeignKey("alumnos.id"), nullable=False)
    accion_key = Column(String, nullable=False)
    puntos_ganados = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)

    alumno = relationship("Alumno")

class GamificacionMedalla(Base):
    __tablename__ = "gamificacion_medallas"
    id = Column(Integer, primary_key=True, index=True)
    inquilino_id = Column(Integer, ForeignKey("inquilinos.id"), nullable=False)
    medalla_key = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    icono_path = Column(String)
    es_manual = Column(Boolean, default=False)

class GamificacionMedallaObtenida(Base):
    __tablename__ = "gamificacion_medallas_obtenidas"
    id = Column(Integer, primary_key=True, index=True)
    inquilino_id = Column(Integer, ForeignKey("inquilinos.id"), nullable=False)
    alumno_id = Column(Integer, ForeignKey("alumnos.id"), nullable=False)
    medalla_key = Column(String, nullable=False)
    fecha_obtencion = Column(DateTime(timezone=True), nullable=False)

    alumno = relationship("Alumno")
