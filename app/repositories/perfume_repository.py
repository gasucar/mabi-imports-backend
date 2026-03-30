from sqlalchemy import Float, cast, func, or_
from sqlalchemy.orm import Session, joinedload
from app.models.perfume import Perfume
from app.models.brand import Brand
from uuid import UUID



class PerfumeRepository:

    def create(self, db: Session, perfume_data):
        perfume = Perfume(**perfume_data)
        db.add(perfume)
        db.commit()
        db.refresh(perfume)
        return perfume


    def get_by_id(self, db: Session, perfume_id: UUID):
        return db.query(Perfume).filter(Perfume.id == perfume_id).first()


    def get_filtered(
        self,
        db,
        page,
        limit,
        search,
        brands,
        gender,
        season,
        intensity,
        price_min,
        price_max
    ):
        query = db.query(Perfume).options(joinedload(Perfume.brand)).join(Perfume.brand)
    
        # 🔎 SEARCH
        if search:
            query = query.filter(Perfume.name.ilike(f"%{search}%"))
    
        # 🏷 BRAND
        if brands:
            brand_list = brands.split(",")
            query = query.filter(Brand.name.in_(brand_list))
    
        # 👤 GENDER
        if gender:
            gender_list = gender.split(",")
            query = query.filter(Perfume.gender_target.in_(gender_list))
    
        # 🌤 SEASON
        if season:
            season_list = season.split(",")
            query = query.filter(Perfume.season.in_(season_list))
    
        # 💥 INTENSITY
        if intensity:
            intensity_list = intensity.split(",")
            query = query.filter(Perfume.intensity.in_(intensity_list))
    
        # 💰 PRICE
        query = query.filter(cast(Perfume.price, Float) >= price_min)
        query = query.filter(cast(Perfume.price, Float) <= price_max)
    
        total = query.count()
    
        data = query.offset((page - 1) * limit).limit(limit).all()
    
        # 🔥 extras
        max_price = db.query(func.max(Perfume.price)).scalar() or 0
    
        brands = (
            db.query(Brand.name)
            .join(Perfume)
            .distinct()
            .all()
        )
    
        brands = [b[0] for b in brands]
    
        return {
            "data": data,
            "total": total,
            "page": page,
            "limit": limit,
            "max_price": max_price,
            "brands": brands,
        }


    def delete(self, db: Session, perfume_id: UUID):
            perfume = self.get_by_id(db, perfume_id)

            if perfume:
                db.delete(perfume)
                db.commit()

            return perfume


    def update(self, db: Session, perfume, data):

        for key, value in data.items():
            setattr(perfume, key, value)

        db.commit()
        db.refresh(perfume)

        return perfume