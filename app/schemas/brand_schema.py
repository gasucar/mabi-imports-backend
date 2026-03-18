from pydantic import BaseModel
from uuid import UUID

class BrandResponse(BaseModel):
    id: UUID
    name: str
    country: str
    description: str
    image: str

    class Config:
        from_attributes = True