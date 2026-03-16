from langchain.tools import tool
from sqlalchemy.orm import Session
from app.models.perfume import Perfume
from app.core.database import SessionLocal


@tool
def search_perfumes(query: str):
    """
    Search perfumes in the database based on a user query.
    """

    db: Session = SessionLocal()

    perfumes = db.query(Perfume).limit(5).all()

    results = []

    for p in perfumes:
        results.append({
            "name": p.name,
            "price": p.price,
            "intensity": p.intensity,
            "season": p.season,
            "description": p.short_description
        })

    db.close()

    return results