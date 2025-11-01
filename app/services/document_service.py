from app.models.models import Document
from sqlalchemy.orm import Session
from app.schemas.document_schema import DocumentCreate


def create(db: Session, payload: DocumentCreate):
    instance = Document(**payload.model_dump())
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def get_all(db: Session):
    return db.query(Document).all()


def get_single(db: Session, id: int):
    return db.query(Document).filter(Document.id == id).first()


def update(db: Session, id: int, payload: DocumentCreate):
    instance = db.query(Document).filter(Document.id == id).first()
    if instance:
        for key, value in payload.model_dump().items():
            setattr(instance, key, value)
        db.commit()
        db.refresh(instance)
    return instance


def delete(db: Session, id: int):
    instance = db.query(Document).filter(Document.id == id).first()
    if instance:
        db.delete(instance)
        db.commit()
    return instance
