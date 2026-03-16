from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.core.database import Base


class Perfume(Base):

    __tablename__ = "perfumes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)

    brand_id = Column(UUID(as_uuid=True), ForeignKey("brands.id"))

    short_description = Column(String)
    long_description = Column(Text)

    price = Column(Float, nullable=False)

    gender_target = Column(String)

    intensity = Column(String)

    season = Column(String)

    duration_hours = Column(Integer)

    stock_quantity = Column(Integer)

    first_image = Column(String)

    images = Column(ARRAY(String))

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow)

    brand = relationship("Brand")

    top = Column(ARRAY(String))
    heart = Column(ARRAY(String))
    base = Column(ARRAY(String))