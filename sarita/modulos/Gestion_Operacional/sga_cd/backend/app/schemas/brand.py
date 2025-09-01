from pydantic import BaseModel
from typing import Dict, Any

class BrandProfileBase(BaseModel):
    tone_of_voice: str | None = "Amistoso, profesional y servicial."
    brand_identity: Dict[str, Any] | None = {}

class BrandProfileCreate(BrandProfileBase):
    pass

class BrandProfileUpdate(BrandProfileBase):
    pass

class BrandProfileInDB(BrandProfileBase):
    id: int
    inquilino_id: int

    class Config:
        from_attributes = True

class BrandProfile(BrandProfileInDB):
    pass
