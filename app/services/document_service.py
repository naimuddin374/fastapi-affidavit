from app.models.models import DocumentModel
from sqlalchemy.orm import Session
from app.schemas.document_schema import DocumentToSaveModel, DocumentCreateReq, DocumentUpdateReq
from app.services.cache_service import CacheService
from app.services.s3_service import S3Service
import mimetypes
from fastapi import Depends,  HTTPException, APIRouter
import os
import json
from app.types.system_types import DocumentStatus, DocumentType
from app.utils.helper import generate_document_file_key
from app.services.rabbitmq_service import rabbitmq_service, OCR_QUEUE_NAME

# Create an instance of the service
s3_service = S3Service()
cache_service = CacheService()

cache_base_key = "documents"


def create(db: Session, payload: DocumentCreateReq):
    payload = DocumentToSaveModel(**payload.model_dump())
    instance = DocumentModel(**payload.model_dump())

    # Convert enm object to sting
    if isinstance(instance.file_type, DocumentType):
        instance.file_type = instance.file_type.value
    if isinstance(instance.status, DocumentStatus):
        instance.status = instance.status.value

    db.add(instance)
    db.commit()
    db.refresh(instance)

    # filename including extension
    file_name = instance.name

    # _, extension = os.path.splitext(file_name)
    mime_type, _ = mimetypes.guess_type(file_name)

    # 10/1-dummy.pdf
    file_key = generate_document_file_key(
        instance.account_id, instance.id, file_name)
    sign_url = s3_service.generate_put_url(
        file_key=file_key, file_type=mime_type)

    instance.sign_url = sign_url

    # Remove old cache
    cache_service.remove_value(cache_base_key)
    return instance


def get_all(db: Session):
    cache_value = cache_service.get_value(cache_base_key)
    if cache_value:
        return cache_value

    response = db.query(DocumentModel).order_by(DocumentModel.id.desc()).all()

    # Set value into cache
    cache_service.set_value(cache_base_key, response)

    return response


def get_single(db: Session, id: int):
    single_key = f"{cache_base_key}:{id}"

    # Check keys exit in cache
    cache_value = cache_service.get_value(single_key)
    if cache_value:
        return cache_value

    response = db.query(DocumentModel).filter(DocumentModel.id == id).first()

    # Generate get sign url
    if response and response.name:
        file_key = generate_document_file_key(
            response.account_id, response.id, response.name)
        response.sign_url = s3_service.generate_get_url(
            file_key=file_key)

    # set value to cache
    cache_service.set_value(single_key, response)

    return response


def update(db: Session, id: int, payload: DocumentUpdateReq):
    instance = db.query(DocumentModel).filter(DocumentModel.id == id).first()
    if instance is None:
        raise HTTPException(status_code=404, detail="Not found")

    for key, value in payload.model_dump(exclude={"name", "account_id"}).items():
        if isinstance(value, DocumentStatus):
            value = value.value
        if isinstance(value, DocumentType):
            value = value.value
        setattr(instance, key, value)
    db.commit()
    db.refresh(instance)

    # Remove old cache
    cache_service.remove_value(f"{cache_base_key}:{id}")
    cache_service.remove_value(cache_base_key)

    # Publish rabbitmq message
    # 1. Create the task message for the OCR worker
    if instance.status == DocumentStatus.UPLOADED.value:
        file_key = f"{instance.account_id}/{instance.id}-{instance.name}"
        s3_key = s3_service.generate_get_url(file_key)
        task_message = {
            "document_id": instance.id,
            "s3_key": s3_key
        }
        print('task_message=', task_message)

        # 2. Publish the message to the queue
        rabbitmq_service.publish_message(
            task_message, queue_name=OCR_QUEUE_NAME)

    return instance


def delete(db: Session, id: int):
    instance = db.query(DocumentModel).filter(DocumentModel.id == id).first()

    if instance is None:
        raise HTTPException(status_code=404, detail="Not found")

    # Delete file from S3 bucket
    if instance.name:
        file_key = generate_document_file_key(
            instance.account_id, instance.id, instance.name)
        result = s3_service.delete_object(file_key=file_key)
        if result == False:
            raise HTTPException(status_code=500, detail="Something went wrong")

    db.delete(instance)
    db.commit()

    # Remove old cache
    cache_service.remove_value(f"{cache_base_key}:{id}")
    cache_service.remove_value(cache_base_key)

    return instance
