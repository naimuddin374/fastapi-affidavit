from models import Transaction
from sqlalchemy.orm import Session
from schemas import TransactionCreate


def create_transaction(db: Session, payload: TransactionCreate):
    instance = Transaction(**payload.model_dump())
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def get_transactions(db: Session):
    return db.query(Transaction).all()


def get_transaction(db: Session, id: int):
    return db.query(Transaction).filter(Transaction.id == id).first()


def update_transaction(db: Session, id: int, payload: TransactionCreate):
    instance = db.query(Transaction).filter(Transaction.id == id).first()
    if instance:
        for key, value in payload.model_dump().items():
            setattr(instance, key, value)
        db.commit()
        db.refresh(instance)
    return instance


def delete_transaction(db: Session, id: int):
    instance = db.query(Transaction).filter(Transaction.id == id).first()
    if instance:
        db.delete(instance)
        db.commit()
    return instance
