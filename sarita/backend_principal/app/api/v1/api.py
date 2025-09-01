from fastapi import APIRouter
from .endpoints import (
    auth,
    tenancy,
    audit,
)

api_router = APIRouter()

# Core API Routers for the Orchestrator
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(tenancy.router, prefix="/tenants", tags=["Tenants"])
api_router.include_router(audit.router, prefix="/audit", tags=["Audit Log"])
