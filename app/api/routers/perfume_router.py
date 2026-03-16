from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.services.perfume_service import PerfumeService
from app.schemas.perfume_schema import PerfumeCreate, PerfumeUpdate, PerfumeResponse


router = APIRouter(prefix="/perfumes", tags=["Perfumes"])

service = PerfumeService()


@router.post("/", response_model=PerfumeResponse)
def create_perfume(perfume: PerfumeCreate, db: Session = Depends(get_db)):
    return service.create_perfume(db, perfume.model_dump())


@router.get("/", response_model=list[PerfumeResponse])
def list_perfumes(db: Session = Depends(get_db)):
    return service.list_perfumes(db)


@router.get("/{perfume_id}", response_model=PerfumeResponse)
def get_perfume(perfume_id: UUID, db: Session = Depends(get_db)):

    perfume = service.get_perfume(db, perfume_id)

    if not perfume:
        raise HTTPException(status_code=404, detail="Perfume not found")

    return perfume


@router.put("/{perfume_id}", response_model=PerfumeResponse)
def update_perfume(
    perfume_id: UUID,
    data: PerfumeUpdate,
    db: Session = Depends(get_db)
):

    perfume = service.update_perfume(db, perfume_id, data.model_dump(exclude_unset=True))

    if not perfume:
        raise HTTPException(status_code=404, detail="Perfume not found")

    return perfume


@router.delete("/{perfume_id}")
def delete_perfume(perfume_id: UUID, db: Session = Depends(get_db)):

    perfume = service.delete_perfume(db, perfume_id)

    if not perfume:
        raise HTTPException(status_code=404, detail="Perfume not found")

    return {"message": "Perfume deleted"}