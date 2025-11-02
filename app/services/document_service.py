from app.models.models import DocumentModel
from sqlalchemy.orm import Session
from app.schemas.document_schema import DocumentToModel, DocumentRequest
from app.services.cache_service import CacheService
from app.services.s3_service import S3Service
import mimetypes
from fastapi import Depends,  HTTPException, APIRouter
import os
import json

# Create an instance of the service
s3_service = S3Service()
cache_service = CacheService()

key = "documents"


def create(db: Session, payload: DocumentRequest):
    payload = DocumentToModel(**payload.model_dump())
    instance = DocumentModel(**payload.model_dump())
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

    instance.name = file_path
    db.commit()
    db.refresh(instance)

    instance.sign_url = sign_url

    # Remove old cache
    cache_service.remove_value(key)
    return instance


def get_all(db: Session):
    cache_value = cache_service.get_value(key)
    if cache_value:
        return cache_value

    response = db.query(DocumentModel).all()

    # Set value into cache
    cache_service.set_value(key, response)

    return response


def get_single(db: Session, id: int):
    single_key = f"{key}:{id}"

    # Check keys exit in cache
    cache_value = cache_service.get_value(single_key)
    if cache_value:
        return cache_value

    response = db.query(DocumentModel).filter(DocumentModel.id == id).first()

    # Generate get sign url
    if response and response.name:
        response.sign_url = s3_service.generate_get_url(
            file_key=response.name)

    # set value to cache
    cache_service.set_value(single_key, response)

    return response


def update(db: Session, id: int, payload: DocumentToModel):
    instance = db.query(DocumentModel).filter(DocumentModel.id == id).first()
    if instance:
        for key, value in payload.model_dump().items():
            setattr(instance, key, value)
        db.commit()
        db.refresh(instance)

        # Remove old cache
        cache_service.remove_value(key)
    return instance


def delete(db: Session, id: int):
    instance = db.query(DocumentModel).filter(DocumentModel.id == id).first()

    if instance is None:
        raise HTTPException(status_code=404, detail="Not found")

    # Delete file from S3 bucket
    if instance.name:
        result = s3_service.delete_object(file_key=instance.name)
        if result == False:
            raise HTTPException(status_code=500, detail="Something went wrong")

    db.delete(instance)
    db.commit()

    # Remove old cache
    cache_service.remove_value(f"{key}:{id}")
    cache_service.remove_value(key)

    return instance
