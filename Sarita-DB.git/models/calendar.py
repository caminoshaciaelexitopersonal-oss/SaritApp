from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class ScheduledPost(Base):
    __tablename__ = 'scheduled_posts'

    id = Column(Integer, primary_key=True, index=True)

    inquilino_id = Column(Integer, ForeignKey('inquilinos.id'), nullable=False, index=True)

    platform = Column(String, nullable=False, index=True)

    # JSON blob to store the content to be published.
    # e.g., {"text": "My amazing post!", "video_url": "...", "title": "..."}
    content_payload = Column(JSON, nullable=False)

    publish_at = Column(DateTime(timezone=True), nullable=False, index=True)

    # Status of the post: 'scheduled', 'publishing', 'published', 'failed'
    status = Column(String, nullable=False, default='scheduled', index=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
