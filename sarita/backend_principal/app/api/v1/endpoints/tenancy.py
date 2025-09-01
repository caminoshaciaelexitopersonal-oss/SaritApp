from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.crud import tenancy as crud_tenancy
from app.api import deps

router = APIRouter()

@router.post("/register", response_model=schemas.tenancy.TenantCreateResponse)
def register_tenant(
    *,
    db: Session = Depends(deps.get_db),
    tenant_in: schemas.tenancy.TenantCreate,
):
    """
    Register a new tenant (company) and its initial admin user.
    """
    try:
        created_tenant = crud_tenancy.create_tenant_and_admin(db=db, obj_in=tenant_in)
        # The admin is attached to the tenant object in the CRUD function
        return {
            "tenant": created_tenant,
            "admin": created_tenant.admin,
        }
    except ValueError as e:
        # This could happen if the role doesn't exist, for example.
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Catch other potential database errors
        raise HTTPException(status_code=500, detail="An unexpected error occurred during registration.")
