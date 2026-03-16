from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.brand import Brand
from app.models.perfume import Perfume
import uuid


def seed():

    db: Session = SessionLocal()

    # ---------- BRANDS ----------

    brands = [
        {"name": "Lattafa", "country": "UAE", "description": "Arabic perfume brand"},
        {"name": "Al Haramain", "country": "UAE", "description": "Luxury Arabic fragrances"},
        {"name": "Afnan", "country": "UAE", "description": "Modern niche inspired perfumes"},
        {"name": "Maison Alhambra", "country": "UAE", "description": "Clone house perfumes"},
    ]

    created_brands = []

    for b in brands:
        existing = db.query(Brand).filter(Brand.name == b["name"]).first()
        brand = Brand(
            id=uuid.uuid4(),
            name=b["name"],
            country=b["country"],
            description=b["description"],
        )

        if not existing:
            db.add(brand)
            created_brands.append(brand)

    db.commit()

    # ---------- PERFUMES ----------

    perfumes = [
        {
            "name": "Asad",
            "brand": created_brands[0],
            "short_description": "Spicy warm fragrance",
            "long_description": "Inspired by Dior Sauvage Elixir",
            "price": 35,
            "gender_target": "male",
            "intensity": "strong",
            "season": "winter",
            "duration_hours": 10,
            "stock_quantity": 100
        },
        {
            "name": "Amber Oud Gold",
            "brand": created_brands[1],
            "short_description": "Sweet fruity fragrance",
            "long_description": "Very long lasting amber fragrance",
            "price": 65,
            "gender_target": "unisex",
            "intensity": "strong",
            "season": "winter",
            "duration_hours": 12,
            "stock_quantity": 80
        },
        {
            "name": "9PM",
            "brand": created_brands[2],
            "short_description": "Sweet vanilla fragrance",
            "long_description": "Inspired by Ultra Male",
            "price": 40,
            "gender_target": "male",
            "intensity": "strong",
            "season": "winter",
            "duration_hours": 9,
            "stock_quantity": 120
        },
        {
            "name": "Kismet Angel",
            "brand": created_brands[3],
            "short_description": "Sweet gourmand fragrance",
            "long_description": "Inspired by Kilian Angels Share",
            "price": 45,
            "gender_target": "unisex",
            "intensity": "strong",
            "season": "winter",
            "duration_hours": 10,
            "stock_quantity": 90
        }
    ]

    for p in perfumes:

        perfume = Perfume(
            id=uuid.uuid4(),
            name=p["name"],
            brand_id=p["brand"].id,
            short_description=p["short_description"],
            long_description=p["long_description"],
            price=p["price"],
            gender_target=p["gender_target"],
            intensity=p["intensity"],
            season=p["season"],
            duration_hours=p["duration_hours"],
            stock_quantity=p["stock_quantity"]
        )

        db.add(perfume)

    db.commit()

    db.close()

    print("Database seeded successfully!")


if __name__ == "__main__":
    seed()