from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.crud.dropdown import crud_dropdowns, CRUDBase

def create_dropdown_router(
    crud_instance: CRUDBase,
    schema: schemas.Dropdown,
    create_schema: schemas.DropdownCreate,
    update_schema: schemas.DropdownUpdate
) -> APIRouter:

    router = APIRouter()

    @router.get("/", response_model=List[schema])
    def read_items(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        # current_user = Depends(deps.get_current_user)
    ) -> Any:
        """
        Retrieve all items for a specific dropdown for the current tenant.
        """
        tenant_id = 1 # Placeholder
        items = crud_instance.get_multi_by_tenant(db, inquilino_id=tenant_id, skip=skip, limit=limit)
        return items

    @router.post("/", response_model=schema)
    def create_item(
        *,
        db: Session = Depends(deps.get_db),
        item_in: create_schema,
    ) -> Any:
        """
        Create a new dropdown item.
        """
        item = crud_instance.create(db=db, obj_in=item_in)
        return item

    @router.put("/{item_id}", response_model=schema)
    def update_item(
        *,
        db: Session = Depends(deps.get_db),
        item_id: int,
        item_in: update_schema,
    ) -> Any:
        """
        Update a dropdown item.
        """
        db_item = crud_instance.get(db=db, id=item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        item = crud_instance.update(db=db, db_obj=db_item, obj_in=item_in)
        return item

    @router.delete("/{item_id}", response_model=schema)
    def delete_item(
        *,
        db: Session = Depends(deps.get_db),
        item_id: int,
    ) -> Any:
        """
        Delete a dropdown item.
        """
        item = crud_instance.remove(db=db, id=item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

    return router

# Create a main router to aggregate all dropdown routers
router = APIRouter()

# Instantiate a sub-router for each dropdown type
for name, crud_obj in crud_dropdowns.items():
    dropdown_specific_router = create_dropdown_router(
        crud_instance=crud_obj,
        schema=schemas.Dropdown,
        create_schema=schemas.DropdownCreate,
        update_schema=schemas.DropdownUpdate
    )
    # Use the name of the dropdown as the prefix for its endpoints
    router.include_router(
        dropdown_specific_router,
        prefix=f"/{name}",
        tags=[f"Dropdown Management: {name.replace('_', ' ').capitalize()}"]
    )
