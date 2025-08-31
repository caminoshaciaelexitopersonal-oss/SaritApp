from sqlalchemy import Column, Integer, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class BrandProfile(Base):
    __tablename__ = 'brand_profiles'

    id = Column(Integer, primary_key=True, index=True)

    # Foreign key to the tenant table
    inquilino_id = Column(Integer, ForeignKey('inquilinos.id'), unique=True, nullable=False, index=True)

    # Tone of voice for the brand
    tone_of_voice = Column(Text, nullable=False, default="Amistoso, profesional y servicial.")

    # JSON blob for storing brand identity elements like logo_url, colors, etc.
    # Example: {"logo_url": "...", "primary_color": "#FFFFFF", "secondary_color": "#000000"}
    brand_identity = Column(JSON, nullable=False, default={})

    # Relationship to the tenant
    inquilino = relationship("Inquilino", back_populates="brand_profile")
