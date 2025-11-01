from app.models.models import Document
from sqlalchemy.orm import Session
from app.schemas.document_schema import DocumentCreate
from app.services.s3_service import S3Service
import mimetypes
import os
import json

# Create an instance of the service
s3_service = S3Service()


def create(db: Session, payload: DocumentCreate):
    instance = Document(**payload.model_dump())
    db.add(instance)
    db.commit()
    db.refresh(instance)

    # filename including extension
    file_name = instance.name

    # _, extension = os.path.splitext(file_name)
    mime_type, _ = mimetypes.guess_type(file_name)

    # 10/1-dummy.pdf
    file_path = f"{instance.account_id}/{instance.id}-{file_name}"
    sign_url = s3_service.generate_put_url(
        file_key=file_path, file_type=mime_type)
    print('sign_url=', sign_url)

    instance.name = file_path
    db.commit()
    db.refresh(instance)

    instance.path = sign_url
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
        # Delete file from S3 bucket
        if instance.name:
            result = s3_service.delete_object(file_key=instance.name)
            print('File deleted successfully from S3 =', instance.name)
            if result == False:
                return False

        db.delete(instance)
        db.commit()

    return instance
