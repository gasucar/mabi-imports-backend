import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class PerfumeNote(Base):
    __tablename__ = "perfume_notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    perfume_id = Column(UUID(as_uuid=True), ForeignKey("perfumes.id"))
    note_id = Column(UUID(as_uuid=True), ForeignKey("notes.id"))

    note_type = Column(String)  # top, heart, base