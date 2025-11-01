from fastapi import Depends,  HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session
from app.core.db import get_db
import app.services.document_service as services
import app.schemas.document_schema as schemas

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


# Routes
@router.get("", response_model=List[schemas.DocumentRead])
def get_all(db: Session = Depends(get_db)):
    return services.get_all(db)


@router.get("/{id}", response_model=schemas.DocumentRead)
def get_single(id: int, db: Session = Depends(get_db)):
    data = services.get_single(db, id)
    if data:
        return data
    raise HTTPException(status_code=404, detail="Not found")


@router.post("", response_model=schemas.DocumentRead)
def create(payload: schemas.DocumentCreate, db: Session = Depends(get_db)):
    return services.create(db, payload)


@router.delete("/{id}", response_model=schemas.DocumentRead)
def delete(id: int, db: Session = Depends(get_db)):
    data = services.delete(db, id)
    if data:
        return data
    raise HTTPException(status_code=404, detail="Not found")
