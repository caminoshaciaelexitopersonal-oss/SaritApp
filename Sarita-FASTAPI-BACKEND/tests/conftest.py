import os
import sys
import pytest
from typing import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Add the directory containing the 'models' package to the Python path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'SGA-CD-DB.git')))

from app.main import app
from app.api import deps
from models.base import Base
import models

# --- Test Database Setup ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Dependency Override ---
def override_get_db() -> Generator:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[deps.get_db] = override_get_db

# --- Test Fixtures ---
@pytest.fixture(scope="function")
def db() -> Generator:
    """
    A fixture that provides a test database session.
    It creates all SQLAlchemy model tables AND the custom RBAC tables.
    """
    # Create tables defined in SQLAlchemy models
    Base.metadata.create_all(bind=engine)

    # Manually create and populate the tables needed for the new RBAC system
    with engine.connect() as connection:
        # Create the roles table
        connection.execute(text("""
            CREATE TABLE roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(50) UNIQUE NOT NULL,
                descripcion TEXT
            )
        """))
        # Create the user_roles join table
        connection.execute(text("""
            CREATE TABLE user_roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES usuarios(id),
                FOREIGN KEY (role_id) REFERENCES roles(id)
            )
        """))
        # Populate the roles table
        connection.execute(text("""
            INSERT INTO roles (nombre, descripcion) VALUES
            ('admin_general', 'Super Administrador del Sistema con acceso total.'),
            ('admin_empresa', 'Administrador de una empresa/inquilino específico.'),
            ('jefe_area', 'Jefe de un área específica como Cultura o Deportes.'),
            ('profesional_area', 'Asistente principal del Jefe de Área.'),
            ('tecnico_area', 'Soporte operativo para un área.'),
            ('coordinador', 'Coordina actividades y al personal de instructores.'),
            ('profesor', 'Instructor o profesor que imparte clases.'),
            ('alumno', 'Estudiante que recibe la formación.'),
            ('padre_acudiente', 'Representante legal de uno o más alumnos.'),
            ('jefe_almacen', 'Gestiona el inventario de materiales y equipos.'),
            ('jefe_escenarios', 'Gestiona la disponibilidad de los espacios físicos.')
        """))
        connection.commit()

    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
        # Drop all tables after the test
        Base.metadata.drop_all(bind=engine)
        # Manually drop the custom tables
        with engine.connect() as connection:
            connection.execute(text("DROP TABLE user_roles"))
            connection.execute(text("DROP TABLE roles"))
            connection.commit()


@pytest.fixture(scope="module")
def client() -> Generator:
    """
    A fixture that provides a TestClient for making requests to the API.
    """
    with TestClient(app) as c:
        yield c
