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


# Get all
@router.get("", response_model=List[schemas.DocumentResponse])
def get_all(db: Session = Depends(get_db)):
    return services.get_all(db)

# Get single


@router.get("/{id}", response_model=schemas.DocumentResponse)
def get_single(id: int, db: Session = Depends(get_db)):
    data = services.get_single(db, id)
    if data:
        return data
    raise HTTPException(status_code=404, detail="Not found")

# Create


@router.post("", response_model=schemas.DocumentResponse)
def create(payload: schemas.DocumentCreateReq, db: Session = Depends(get_db)):
    return services.create(db, payload)

# Update


@router.put("/{id}", response_model=schemas.DocumentResponse)
def update(id: int, payload: schemas.DocumentUpdateReq, db: Session = Depends(get_db)):
    return services.update(db, id, payload)


# Delete
@router.delete("/{id}", response_model=schemas.DocumentResponse)
def delete(id: int, db: Session = Depends(get_db)):
    data = services.delete(db, id)
    if data:
        return data
    raise HTTPException(status_code=404, detail="Not found")
