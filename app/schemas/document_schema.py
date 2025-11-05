import datetime
from pydantic import BaseModel, Field
from typing import Optional
from app.types.system_types import DocumentType, DocumentStatus

# phone: Field(pattern=fr"\+880-\d{10}")


class DocumentCreateReq(BaseModel):
    name: str = Field(
        examples=["dummy.pdf"], description="Name of the file including extension")
    account_id: int = Field(examples=[1], description="Selected account ID")
    file_type: DocumentType = Field(default=DocumentType.STATEMENT, examples=[DocumentType.STATEMENT.value],
                                    description="Document type")


class DocumentToSaveModel(DocumentCreateReq):
    status: DocumentStatus = Field(default=DocumentStatus.PENDING, examples=[DocumentStatus.PENDING.value],
                                   description="Document status")
    pass


class DocumentUpdateReq(BaseModel):
    file_type: DocumentType = Field(default=DocumentType.STATEMENT, examples=[DocumentType.STATEMENT.value],
                                    description="Document type")
    status: DocumentStatus = Field(default=DocumentStatus.PENDING, examples=[DocumentStatus.PENDING.value],
                                   description="Document status")
    pass


class DocumentResponse(DocumentCreateReq):
    id: int
    file_type: Optional[DocumentType] = None
    status: Optional[DocumentStatus] = None
    sign_url: Optional[str] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class config:
        # orm_mode = True # pydantic version < 2.x
        from_attribute = True
