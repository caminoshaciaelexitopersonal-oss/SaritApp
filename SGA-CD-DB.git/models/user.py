import enum
from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Enum as SQLAlchemyEnum
)
from sqlalchemy.orm import relationship
from .base import Base
from .area import usuario_areas_association # Import the association table

class RolesEnum(enum.Enum):
    admin_general = "admin_general"
    admin_empresa = "admin_empresa"
    jefe_area = "jefe_area"
    coordinador = "coordinador"
    profesor = "profesor"
    alumno = "alumno"
    almacenista = "almacenista"
    jefe_almacen = "jefe_almacen"
    jefe_escenarios = "jefe_escenarios"
    profesional_cultura = "profesional_cultura"
    profesional_deportes = "profesional_deportes"
    tecnico_cultura = "tecnico_cultura"
    tecnico_deportes = "tecnico_deportes"
    asistencial_cultura = "asistencial_cultura"
    asistencial_deportes = "asistencial_deportes"
    instructor_cultura = "instructor_cultura"
    instructor_deportes = "instructor_deportes"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    inquilino_id = Column(Integer, ForeignKey("inquilinos.id"), nullable=False)
    nombre_usuario = Column(String, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    rol = Column(SQLAlchemyEnum(RolesEnum), nullable=False)
    nombre_completo = Column(String)
    correo = Column(String, unique=True, index=True)
    reporta_a_usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    reset_token = Column(String)
    reset_token_expires = Column(DateTime(timezone=True))
    activo = Column(Boolean, default=True)
    dashboard_layout = Column(Text)

    # Relationships
    inquilino = relationship("Inquilino")
    superior = relationship("Usuario", remote_side=[id], backref="subordinados")

    # Many-to-many relationship with Area
    areas = relationship("Area", secondary=usuario_areas_association, backref="usuarios")

    # One-to-one relationships for role-specific details
    profesor_details = relationship("Profesor", back_populates="usuario", uselist=False, cascade="all, delete-orphan")
    alumno_details = relationship("Alumno", back_populates="usuario", uselist=False, cascade="all, delete-orphan")
    jefe_area_details = relationship("JefeArea", back_populates="usuario", uselist=False, cascade="all, delete-orphan")
    coordinador_details = relationship("Coordinador", back_populates="usuario", uselist=False, cascade="all, delete-orphan")
    almacenista_details = relationship("Almacenista", back_populates="usuario", uselist=False, cascade="all, delete-orphan")
    jefe_almacen_details = relationship("JefeAlmacen", back_populates="usuario", uselist=False, cascade="all, delete-orphan")
    jefe_escenarios_details = relationship("JefeEscenarios", back_populates="usuario", uselist=False, cascade="all, delete-orphan")


class Profesor(Base):
    __tablename__ = "profesores"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True, nullable=False)
    inquilino_id = Column(Integer, ForeignKey("inquilinos.id"), nullable=False)
    # The 'area' column is now removed. Area is managed via the 'usuario.areas' relationship.
    telefono = Column(String)
    usuario = relationship("Usuario", back_populates="profesor_details")

class JefeArea(Base):
    __tablename__ = "jefes_area"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True, nullable=False)
    inquilino_id = Column(Integer, ForeignKey("inquilinos.id"), nullable=False)
    # The 'area_responsabilidad' column is removed. Area is managed via the 'usuario.areas' relationship.
    usuario = relationship("Usuario", back_populates="jefe_area_details")

class Coordinador(Base):
    __tablename__ = "coordinadores"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True, nullable=False)
    inquilino_id = Column(Integer, ForeignKey("inquilinos.id"), nullable=False)
    jefe_area_id = Column(Integer, ForeignKey("jefes_area.id"))
    usuario = relationship("Usuario", back_populates="coordinador_details")
    jefe_area = relationship("JefeArea")

class JefeAlmacen(Base):
    __tablename__ = "jefes_almacen"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True, nullable=False)
    inquilino_id = Column(Integer, ForeignKey("inquilinos.id"), nullable=False)
    usuario = relationship("Usuario", back_populates="jefe_almacen_details")

class JefeEscenarios(Base):
    __tablename__ = "jefes_escenarios"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True, nullable=False)
    inquilino_id = Column(Integer, ForeignKey("inquilinos.id"), nullable=False)
    usuario = relationship("Usuario", back_populates="jefe_escenarios_details")

class Alumno(Base):
    __tablename__ = "alumnos"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True, nullable=False)
    inquilino_id = Column(Integer, ForeignKey("inquilinos.id"), nullable=False)
    tipo_documento = Column(String)
    documento = Column(String, index=True)
    fecha_nacimiento = Column(DateTime(timezone=True))
    genero = Column(String)
    grupo_etario = Column(String)
    escolaridad = Column(String)
    discapacidad = Column(String)
    grupo_poblacional = Column(String)
    barrio = Column(String)
    vereda = Column(String)
    resguardo = Column(String)
    zona_geografica = Column(String)
    telefono = Column(String)
    puntos_totales = Column(Integer, default=0)
    nivel = Column(Integer, default=1)
    mostrar_en_rankings = Column(Boolean, default=True)
    usuario = relationship("Usuario", back_populates="alumno_details")

class Almacenista(Base):
    __tablename__ = "almacenistas"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True, nullable=False)
    inquilino_id = Column(Integer, ForeignKey("inquilinos.id"), nullable=False)
    area_almacen = Column(String)
    usuario = relationship("Usuario", back_populates="almacenista_details")
