from sqlalchemy.orm import Session
import uuid

from app.models.brand import Brand
from app.models.perfume import Perfume
from app.core.database import SessionLocal


def seed():

    db: Session = SessionLocal()

    print("Seeding database...")

    # -------------------------
    # BRANDS
    # -------------------------

    brands_data = [
        "Lattafa",
        "Al Haramain",
        "Afnan",
        "Maison Alhambra"
    ]

    brands = {}

    for brand_name in brands_data:

        existing = db.query(Brand).filter(Brand.name == brand_name).first()

        if existing:
            brands[brand_name] = existing
            continue

        brand = Brand(
            id=uuid.uuid4(),
            name=brand_name,
            country="UAE",
            description=f"{brand_name} Arabic fragrance house"
        )

        db.add(brand)
        brands[brand_name] = brand

    db.commit()

    # -------------------------
    # PERFUMES
    # -------------------------

    perfumes = [
        {
            "name": "Lattafa Asad",
            "brand": "Lattafa",
            "price": 35,
            "image": "https://http2.mlstatic.com/D_NQ_NP_704992-MLA83637592590_042025-O.webp",
            "images": [
                "https://http2.mlstatic.com/D_NQ_NP_704992-MLA83637592590_042025-O.webp"
            ],
            "top": ["black pepper", "pineapple", "tobacco"],
            "heart": ["coffee", "patchouli", "iris"],
            "base": ["vanilla", "amber", "dry woods"],
            "description": "Warm spicy fragrance inspired by Dior Sauvage Elixir"
        },
        {
            "name": "Afnan 9PM",
            "brand": "Afnan",
            "price": 40,
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQpBXcjtkjgWK36LQuwsmoesoK7WACk9Hyyw&s",
            "images": [
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQpBXcjtkjgWK36LQuwsmoesoK7WACk9Hyyw&s"
            ],
            "top": ["apple", "cinnamon", "lavender"],
            "heart": ["orange blossom"],
            "base": ["vanilla", "tonka bean", "amber"],
            "description": "Sweet vanilla night fragrance inspired by Ultra Male"
        },
        {
            "name": "Al Haramain Amber Oud Gold",
            "brand": "Al Haramain",
            "price": 65,
            "image": "https://dcdn-us.mitiendanube.com/stores/005/511/767/products/5-dcce6cc39991428ac417325875694545-1024-1024.webp",
            "images": [
                "https://dcdn-us.mitiendanube.com/stores/005/511/767/products/5-dcce6cc39991428ac417325875694545-1024-1024.webp"
            ],
            "top": ["bergamot", "green notes"],
            "heart": ["melon", "pineapple"],
            "base": ["amber", "vanilla", "musk"],
            "description": "Extremely sweet fruity amber fragrance"
        },
        {
            "name": "Maison Alhambra Kismet Angel",
            "brand": "Maison Alhambra",
            "price": 45,
            "image": "https://http2.mlstatic.com/D_NQ_NP_612757-MLA77456647446_072024-O.webp",
            "images": [
                "https://http2.mlstatic.com/D_NQ_NP_612757-MLA77456647446_072024-O.webp"
            ],
            "top": ["cognac"],
            "heart": ["cinnamon", "tonka bean"],
            "base": ["vanilla", "oak", "praline"],
            "description": "Inspired by Kilian Angel's Share"
        },
        {
            "name": "Lattafa Khamrah",
            "brand": "Lattafa",
            "price": 50,
            "image": "https://http2.mlstatic.com/D_NQ_NP_885438-MLA72879950179_112023-O.webp",
            "images": [
                "https://http2.mlstatic.com/D_NQ_NP_885438-MLA72879950179_112023-O.webp"
            ],
            "top": ["cinnamon", "nutmeg", "bergamot"],
            "heart": ["dates", "praline", "tuberose"],
            "base": ["vanilla", "tonka bean", "amberwood"],
            "description": "Sweet boozy gourmand winter fragrance"
        },
        {
            "name": "Lattafa Yara Rosa",
            "brand": "Lattafa",
            "price": 30,
            "image": "https://acdn-us.mitiendanube.com/stores/004/407/494/products/yara-cde4579cb71070a8c617135640512548-1024-1024.webp",
            "images": [
                "https://acdn-us.mitiendanube.com/stores/004/407/494/products/yara-cde4579cb71070a8c617135640512548-1024-1024.webp"
            ],
            "top": ["heliotrope", "orchid"],
            "heart": ["tropical fruits"],
            "base": ["vanilla", "musk", "sandalwood"],
            "description": "Sweet creamy feminine fragrance"
        },
        {
            "name": "Afnan Turathi Blue",
            "brand": "Afnan",
            "price": 55,
            "image": "https://fimgs.net/mdimg/perfume/375x500.70304.jpg",
            "images": [
                "https://fimgs.net/mdimg/perfume/375x500.70304.jpg"
            ],
            "top": ["bergamot", "grapefruit"],
            "heart": ["amberwood"],
            "base": ["musk", "patchouli"],
            "description": "Fresh citrus woody fragrance"
        },
        {
            "name": "Maison Alhambra Porto Neroli",
            "brand": "Maison Alhambra",
            "price": 35,
            "image": "https://fimgs.net/mdimg/perfume/375x500.70412.jpg",
            "images": [
                "https://fimgs.net/mdimg/perfume/375x500.70412.jpg"
            ],
            "top": ["neroli", "bergamot"],
            "heart": ["orange blossom"],
            "base": ["musk", "amber"],
            "description": "Inspired by Tom Ford Neroli Portofino"
        },
        {
            "name": "Lattafa Fakhar Black",
            "brand": "Lattafa",
            "price": 38,
            "image": "https://fimgs.net/mdimg/perfume/375x500.64853.jpg",
            "images": [
                "https://fimgs.net/mdimg/perfume/375x500.64853.jpg"
            ],
            "top": ["apple", "ginger", "bergamot"],
            "heart": ["lavender", "sage"],
            "base": ["tonka bean", "amberwood"],
            "description": "Inspired by YSL Y"
        },
        {
            "name": "Al Haramain Detour Noir",
            "brand": "Al Haramain",
            "price": 45,
            "image": "https://fimgs.net/mdimg/perfume/375x500.70740.jpg",
            "images": [
                "https://fimgs.net/mdimg/perfume/375x500.70740.jpg"
            ],
            "top": ["apple", "lavender"],
            "heart": ["violet", "jasmine"],
            "base": ["vanilla", "sandalwood"],
            "description": "Inspired by Parfums de Marly Layton"
        }
    ]

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

            gender_target="unisex",

            intensity="medium",

            season="all",

            duration_hours=8,

            stock_quantity=10,  # 👈 lo cambiamos a 10

            first_image=p["image"],

            images=p["images"],

            top=p["top"],

            heart=p["heart"],

            base=p["base"]

        )

        db.add(perfume)

    db.commit()

    db.close()

    print("Database seeded successfully!")


if __name__ == "__main__":
    seed()