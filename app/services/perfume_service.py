from sqlalchemy.orm import Session
from app.repositories.perfume_repository import PerfumeRepository


class PerfumeService:

    def __init__(self):
        self.repository = PerfumeRepository()


    def create_perfume(self, db: Session, perfume_data):
        return self.repository.create(db, perfume_data)


    def get_perfume(self, db: Session, perfume_id):
        return self.repository.get_by_id(db, perfume_id)


    def list_perfumes(self, db: Session, page: int, limit: int, search: str | None):
        return self.repository.get_all(db, page, limit, search)


    def delete_perfume(self, db: Session, perfume_id):
        return self.repository.delete(db, perfume_id)


    def update_perfume(self, db: Session, perfume_id, data):

        perfume = self.repository.get_by_id(db, perfume_id)

        if not perfume:
            return None

        return self.repository.update(db, perfume, data)