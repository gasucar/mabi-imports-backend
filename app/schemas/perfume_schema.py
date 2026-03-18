from pydantic import BaseModel
from uuid import UUID
from typing import Optional

from app.schemas.brand_schema import BrandResponse


class PerfumeBase(BaseModel):
    name: str
    brand: Optional[BrandResponse]
    short_description: Optional[str]
    long_description: Optional[str]
    price: str
    gender_target: Optional[str]
    intensity: Optional[str]
    season: Optional[str]
    duration_hours: Optional[str]
    stock_quantity: Optional[str]
    first_image: Optional[str]
    images: Optional[list[str]]


class PerfumeCreate(PerfumeBase):
    pass


class PerfumeUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]
    stock_quantity: Optional[int]


class PerfumeResponse(PerfumeBase):
    id: UUID

    class Config:
        from_attributes = True