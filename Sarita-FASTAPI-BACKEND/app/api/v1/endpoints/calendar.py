from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
import models
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.ScheduledPost])
def read_scheduled_posts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.Usuario = Depends(deps.get_current_active_user),
):
    """
    Retrieve scheduled posts for the current user's tenant.
    """
    posts = crud.scheduled_post.get_multi_by_tenant(
        db, inquilino_id=current_user.inquilino_id, skip=skip, limit=limit
    )
    return posts

@router.post("/", response_model=schemas.ScheduledPost)
def create_scheduled_post(
    *,
    db: Session = Depends(deps.get_db),
    post_in: schemas.ScheduledPostCreate,
    current_user: models.user.Usuario = Depends(deps.get_current_active_user),
):
    """
    Create a new scheduled post for the current user's tenant.
    """
    post = crud.scheduled_post.create_with_tenant(
        db=db, obj_in=post_in, inquilino_id=current_user.inquilino_id
    )
    return post

@router.put("/{post_id}", response_model=schemas.ScheduledPost)
def update_scheduled_post(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    post_in: schemas.ScheduledPostUpdate,
    current_user: models.user.Usuario = Depends(deps.get_current_active_user),
):
    """
    Update a scheduled post.
    """
    post = crud.scheduled_post.get(db=db, id=post_id)
    if not post or post.inquilino_id != current_user.inquilino_id:
        raise HTTPException(status_code=404, detail="Scheduled post not found")

    post = crud.scheduled_post.update(db=db, db_obj=post, obj_in=post_in)
    return post

@router.delete("/{post_id}", response_model=schemas.ScheduledPost)
def delete_scheduled_post(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    current_user: models.user.Usuario = Depends(deps.get_current_active_user),
):
    """
    Delete a scheduled post.
    """
    post = crud.scheduled_post.get(db=db, id=post_id)
    if not post or post.inquilino_id != current_user.inquilino_id:
        raise HTTPException(status_code=404, detail="Scheduled post not found")

    post = crud.scheduled_post.remove(db=db, id=post_id)
    return post
