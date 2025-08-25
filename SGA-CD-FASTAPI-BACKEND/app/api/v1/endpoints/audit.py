from typing import List, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.AuditLog])
def read_audit_logs(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user = Depends(deps.get_current_active_user) # TODO: Add admin role check
) -> Any:
    """
    Retrieve audit logs for the current user's tenant.
    This should be restricted to admin users.
    """
    tenant_id = 1 # Placeholder for current_user.inquilino_id
    logs = crud.audit.get_audit_logs_by_tenant(
        db, inquilino_id=tenant_id, skip=skip, limit=limit
    )
    return logs
