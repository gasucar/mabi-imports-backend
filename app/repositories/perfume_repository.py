from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload
from app.models.perfume import Perfume
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


    def get_all(self, db: Session, page: int, limit: int, search: str | None):
        query = db.query(Perfume).options(joinedload(Perfume.brand))

        # 🔍 SEARCH
        if search:
            query = query.filter(
                or_(
                    Perfume.name.ilike(f"%{search}%"),
                    Perfume.short_description.ilike(f"%{search}%"),
                )
            )

        # 🔢 TOTAL
        total = query.count()

        # 📄 PAGINATION
        offset = (page - 1) * limit

        perfumes = (
            query
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "data": perfumes,
            "total": total,
            "page": page,
            "limit": limit
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