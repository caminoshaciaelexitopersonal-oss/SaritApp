from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

class ScheduledPostBase(BaseModel):
    platform: str
    content_payload: Dict[str, Any]
    publish_at: datetime
    status: str | None = 'scheduled'

class ScheduledPostCreate(ScheduledPostBase):
    pass

class ScheduledPostUpdate(BaseModel):
    publish_at: datetime | None = None
    status: str | None = None
    content_payload: Dict[str, Any] | None = None

class ScheduledPostInDB(ScheduledPostBase):
    id: int
    inquilino_id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True

class ScheduledPost(ScheduledPostInDB):
    pass
