import sys
import os
from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings

# This path adjustment points to the unified database models directory
db_repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'base_datos', 'unificada'))
if db_repo_path not in sys.path:
    sys.path.insert(0, db_repo_path)

from app.db.session import engine
from models.base import Base

# This could be managed by Alembic in the future
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sarita - Backend Principal (Orchestrator)")

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "Sarita Orchestrator is running"}
