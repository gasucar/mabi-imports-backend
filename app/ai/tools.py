import os
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select, cast, Integer

from app.models.perfume import Perfume
from app.core.database import SessionLocal

# Notas
SWEET_NOTES = ["vanilla", "tonka", "praline", "caramel", "sugar", "chocolate", "dates"]
FRESH_NOTES = ["citrus", "lemon", "bergamot", "orange", "grapefruit"]
WOODY_NOTES = ["sandalwood", "cedar", "oud", "patchouli"]

# Tool de búsqueda
def perfume_matches(perfume, query: str) -> bool:
    notes = (perfume.top or []) + (perfume.heart or []) + (perfume.base or [])
    notes_text = " ".join(notes).lower()
    query = query.lower()
    if "fresh" in query or "fresco" in query:
        if any(note in notes_text for note in FRESH_NOTES):
            return True
    if "sweet" in query or "dulce" in query:
        if any(note in notes_text for note in SWEET_NOTES):
            return True
    if "woody" in query:
        if any(note in notes_text for note in WOODY_NOTES):
            return True
    if perfume.season and perfume.season.lower() in query:
        return True
    return False

def serialize_perfume(perfume) -> dict:
    return {
        "id": perfume.id,
        "name": perfume.name,
        "brand": perfume.brand,
        "short_description": perfume.short_description,
        "duration": perfume.duration_hours,
        "intensity": perfume.intensity,
        "first_image": perfume.first_image,
        "url": f"{os.getenv('FRONTEND_URL')}/perfumes/{perfume.id}"
    }

# Tool compatible con agente
def search_perfumes(query: str) -> List[dict]:
    """
    Busca perfumes en stock según la query y devuelve como lista de diccionarios serializables.
    """
    db: Session = SessionLocal()
    try:
        perfumes = db.execute(select(Perfume).where(cast(Perfume.stock_quantity, Integer) > 0)).scalars().all()
        results = [serialize_perfume(p) for p in perfumes if perfume_matches(p, query)]
        return results[:3]  # máximo 3 perfumes
    finally:
        db.close()