from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated, List, Optional
from sqlalchemy.orm import Session
from db import get_db, engine
import services
import models
import schemas


# App
app = FastAPI()

# Routes


@app.get('/')
def index():
    return {"message": "Welcome to FastApi"}


@app.get("/transactions", response_model=List[schemas.Transaction])
def add_transactions(db: Session = Depends(get_db)):
    return services.get_transactions(db)


@app.get("/transactions/{id}", response_model=schemas.Transaction)
def add_transactions(id: int, db: Session = Depends(get_db)):
    data = services.get_transaction(db, id)
    if data:
        return data
    raise HTTPException(status_code=404, detail="Not found")


@app.post("/transactions", response_model=schemas.Transaction)
def create_transactions(payload: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return services.create_transaction(db, payload)


@app.put("/transactions/{id}", response_model=schemas.Transaction)
def update_transactions(id: int, payload: schemas.TransactionCreate, db: Session = Depends(get_db)):
    db_update = services.update_transaction(db, id, payload)
    if db_update:
        return db_update
    raise HTTPException(status_code=404, detail="Not found")


@app.delete("/transactions/{id}", response_model=schemas.Transaction)
def delete_transactions(id: int, db: Session = Depends(get_db)):
    data = services.delete_transaction(db, id)
    if data:
        return data
    raise HTTPException(status_code=404, detail="Not found")
