from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class PerfumeBase(BaseModel):
    name: str
    brand_id: UUID
    short_description: Optional[str]
    long_description: Optional[str]
    price: float
    gender_target: Optional[str]
    intensity: Optional[str]
    season: Optional[str]
    duration_hours: Optional[int]
    stock_quantity: Optional[int]


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