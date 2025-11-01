from app.models.models import Transaction
from sqlalchemy.orm import Session
from app.schemas.transaction_schema import TransactionCreate


def create(db: Session, payload: TransactionCreate):
    instance = Transaction(**payload.model_dump())
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def get_all(db: Session):
    return db.query(Transaction).all()


def get_single(db: Session, id: int):
    return db.query(Transaction).filter(Transaction.id == id).first()


def update(db: Session, id: int, payload: TransactionCreate):
    instance = db.query(Transaction).filter(Transaction.id == id).first()
    if instance:
        for key, value in payload.model_dump().items():
            setattr(instance, key, value)
        db.commit()
        db.refresh(instance)
    return instance


def delete(db: Session, id: int):
    instance = db.query(Transaction).filter(Transaction.id == id).first()
    if instance:
        db.delete(instance)
        db.commit()
    return instance
