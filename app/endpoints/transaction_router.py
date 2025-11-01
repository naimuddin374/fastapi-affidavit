from fastapi import Depends,  HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session
from app.core.db import get_db
import app.services.transaction_service as services
import app.schemas.transaction_schema as schemas

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


# Routes
@router.get("", response_model=List[schemas.Transaction])
def get_all(db: Session = Depends(get_db)):
    return services.get_all(db)


@router.get("/{id}", response_model=schemas.Transaction)
def get_single(id: int, db: Session = Depends(get_db)):
    data = services.get_single(db, id)
    if data:
        return data
    raise HTTPException(status_code=404, detail="Not found")


@router.post("", response_model=schemas.Transaction)
def create(payload: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return services.create(db, payload)


@router.put("/{id}", response_model=schemas.Transaction)
def update(id: int, payload: schemas.TransactionCreate, db: Session = Depends(get_db)):
    db_update = services.update(db, id, payload)
    if db_update:
        return db_update
    raise HTTPException(status_code=404, detail="Not found")


@router.delete("/{id}", response_model=schemas.Transaction)
def delete(id: int, db: Session = Depends(get_db)):
    data = services.delete(db, id)
    if data:
        return data
    raise HTTPException(status_code=404, detail="Not found")
