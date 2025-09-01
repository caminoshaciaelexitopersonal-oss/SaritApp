import sys
import os

# Workaround for environment's PYTHONPATH issues.
# Adds Sarita-DB.git directory to the path to allow model imports.
db_repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Sarita-DB.git'))
if db_repo_path not in sys.path:
    sys.path.insert(0, db_repo_path)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import engine
# Note: The path to models is added in run_server.py, so this import should work.
from models.base import Base

# Create database tables
# This will create the tables if they don't exist, including the sga_cd.db file for SQLite
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# Create static directory if it doesn't exist
static_dir = "app/static"
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
