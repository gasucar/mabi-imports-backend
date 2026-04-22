
import uuid

from fastapi import APIRouter
from requests import Session

from backend.app.core.database import SessionLocal
from backend.app.models.brand import Brand
from backend.app.models.perfume import Perfume


router = APIRouter(prefix="/seed", tags=["seed"])

@router.post("/seed")
def seed_database():

    db: Session = SessionLocal()

    try:
        print("Seeding database...")

        # -------------------------
        # BRANDS
        # -------------------------
        brands_data = [
            {"name": "Lattafa", "image": "https://1000logos.net/wp-content/uploads/2023/03/Lattafa-Logo.png"},
            {"name": "Al Haramain", "image": "https://1000logos.net/wp-content/uploads/2023/03/Al-Haramain-Logo.png"},
            {"name": "Afnan", "image": "https://1000logos.net/wp-content/uploads/2023/03/Afnan-Logo.png"},
            {"name": "Maison Alhambra", "image": "https://1000logos.net/wp-content/uploads/2023/03/Maison-Alhambra-Logo.png"}
        ]

        brands = {}

        for b in brands_data:
            existing = db.query(Brand).filter(Brand.name == b["name"]).first()

            if existing:
                brands[b["name"]] = existing
                continue

            brand = Brand(
                id=uuid.uuid4(),
                name=b["name"],
                image=b["image"],
                country="UAE",
                description=f"{b['name']} Arabic fragrance house"
            )

            db.add(brand)
            db.flush()  # 👈 IMPORTANTE para obtener ID sin commit
            brands[b["name"]] = brand

        # -------------------------
        # PERFUMES
        # -------------------------
        perfumes = [
            {
                "name": "Lattafa Asad",
                "brand": "Lattafa",
                "price": "35000",
                "duration": "8h",
                "stock": "10",
                "image": "https://http2.mlstatic.com/D_NQ_NP_704992-MLA83637592590_042025-O.webp",
                "images": ["https://http2.mlstatic.com/D_NQ_NP_704992-MLA83637592590_042025-O.webp"],
                "top": ["black pepper", "pineapple", "tobacco"],
                "heart": ["coffee", "patchouli", "iris"],
                "base": ["vanilla", "amber", "dry woods"],
                "description": "Warm spicy fragrance inspired by Dior Sauvage Elixir"
            },
            {
                "name": "Afnan 9PM",
                "brand": "Afnan",
                "price": "40000",
                "duration": "10h",
                "stock": "8",
                "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQpBXcjtkjgWK36LQuwsmoesoK7WACk9Hyyw&s",
                "images": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQpBXcjtkjgWK36LQuwsmoesoK7WACk9Hyyw&s"],
                "top": ["apple", "cinnamon", "lavender"],
                "heart": ["orange blossom"],
                "base": ["vanilla", "tonka bean", "amber"],
                "description": "Sweet vanilla night fragrance inspired by Ultra Male"
            },
            {
                "name": "Al Haramain Amber Oud Gold",
                "brand": "Al Haramain",
                "price": "65000",
                "duration": "12h",
                "stock": "5",
                "image": "https://dcdn-us.mitiendanube.com/stores/005/511/767/products/5-dcce6cc39991428ac417325875694545-1024-1024.webp",
                "images": ["https://dcdn-us.mitiendanube.com/stores/005/511/767/products/5-dcce6cc39991428ac417325875694545-1024-1024.webp"],
                "top": ["bergamot", "green notes"],
                "heart": ["melon", "pineapple"],
                "base": ["amber", "vanilla", "musk"],
                "description": "Extremely sweet fruity amber fragrance"
            },
            {
                "name": "Maison Alhambra Kismet Angel",
                "brand": "Maison Alhambra",
                "price": "45000",
                "duration": "9h",
                "stock": "7",
                "image": "https://http2.mlstatic.com/D_NQ_NP_612757-MLA77456647446_072024-O.webp",
                "images": ["https://http2.mlstatic.com/D_NQ_NP_612757-MLA77456647446_072024-O.webp"],
                "top": ["cognac"],
                "heart": ["cinnamon", "tonka bean"],
                "base": ["vanilla", "oak", "praline"],
                "description": "Inspired by Kilian Angel's Share"
            },
            {
                "name": "Lattafa Khamrah",
                "brand": "Lattafa",
                "price": "50000",
                "duration": "12h",
                "stock": "6",
                "image": "https://http2.mlstatic.com/D_NQ_NP_885438-MLA72879950179_112023-O.webp",
                "images": ["https://http2.mlstatic.com/D_NQ_NP_885438-MLA72879950179_112023-O.webp"],
                "top": ["cinnamon", "nutmeg", "bergamot"],
                "heart": ["dates", "praline", "tuberose"],
                "base": ["vanilla", "tonka bean", "amberwood"],
                "description": "Sweet boozy gourmand winter fragrance"
            },
            {
                "name": "Lattafa Yara Rosa",
                "brand": "Lattafa",
                "price": "30000",
                "duration": "6h",
                "stock": "12",
                "image": "https://acdn-us.mitiendanube.com/stores/004/407/494/products/yara-cde4579cb71070a8c617135640512548-1024-1024.webp",
                "images": ["https://acdn-us.mitiendanube.com/stores/004/407/494/products/yara-cde4579cb71070a8c617135640512548-1024-1024.webp"],
                "top": ["heliotrope", "orchid"],
                "heart": ["tropical fruits"],
                "base": ["vanilla", "musk", "sandalwood"],
                "description": "Sweet creamy feminine fragrance"
            }
        ]

        created = 0

        for p in perfumes:
            existing = db.query(Perfume).filter(Perfume.name == p["name"]).first()

            if existing:
                continue

            perfume = Perfume(
                id=uuid.uuid4(),
                name=p["name"],
                brand_id=brands[p["brand"]].id,
                short_description=p["description"],
                long_description=p["description"],
                price=p["price"],
                stock_quantity=p["stock"],
                duration_hours=p["duration"],
                gender_target="unisex",
                intensity="medium",
                season="all",
                first_image=p["image"],
                images=p["images"],
                top=p["top"],
                heart=p["heart"],
                base=p["base"]
            )

            db.add(perfume)
            created += 1

        db.commit()

        return {
            "message": "Database seeded successfully",
            "perfumes_created": created
        }

    except Exception as e:
        db.rollback()
        return {"error": str(e)}

    finally:
        db.close()