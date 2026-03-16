import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.core.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    perfume_id = Column(UUID(as_uuid=True), ForeignKey("perfumes.id"))

    rating = Column(Integer)

    comment_text = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)