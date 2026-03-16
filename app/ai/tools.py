from langchain_core.tools import tool
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.perfume import Perfume
from app.core.database import SessionLocal


SWEET_NOTES = [
    "vanilla",
    "tonka",
    "praline",
    "caramel",
    "sugar",
    "chocolate",
    "dates"
]

FRESH_NOTES = [
    "citrus",
    "lemon",
    "bergamot",
    "orange",
    "grapefruit"
]

WOODY_NOTES = [
    "sandalwood",
    "cedar",
    "oud",
    "patchouli"
]


def perfume_matches(perfume, query):

    notes = (
        (perfume.top or [])
        + (perfume.heart or [])
        + (perfume.base or [])
    )

    notes_text = " ".join(notes).lower()

    query = query.lower()

    if "sweet" in query or "dulce" in query:
        if any(note in notes_text for note in SWEET_NOTES):
            return True

    if "fresh" in query or "fresco" in query:
        if any(note in notes_text for note in FRESH_NOTES):
            return True

    if "woody" in query:
        if any(note in notes_text for note in WOODY_NOTES):
            return True

    if perfume.season and perfume.season.lower() in query:
        return True

    return False


def serialize_perfume(perfume):

    return {
        "id": perfume.id,
        "name": perfume.name,
        "brand": perfume.brand,
        "short_description": perfume.short_description,
        "duration": perfume.duration_hours,
        "intensity": perfume.intensity,
        "first_image": perfume.first_image,
        "url": f"/perfumes/{perfume.id}"
    }


@tool
def search_perfumes(query: str) -> list:
    
    """
    Search perfumes available in the store inventory.

    The query may include:
    - fragrance style (sweet, fresh, woody)
    - season (winter, summer)
    - intensity (strong, soft)
    - duration (long lasting)

    Return a list of perfumes that match the user request.
    """

    db: Session = SessionLocal()

    try:

        perfumes = db.execute(
            select(Perfume).where(Perfume.stock_quantity > 0)
        ).scalars().all()

        results = []

        for perfume in perfumes:

            if perfume_matches(perfume, query):
                results.append(serialize_perfume(perfume))

        return results[:3]

    finally:

        db.close()