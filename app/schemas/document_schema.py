import datetime
from pydantic import BaseModel, Field
from typing import Optional
from app.types.system_types import DocumentType, DocumentStatus

# phone: Field(pattern=fr"\+880-\d{10}")


class DocumentRequest(BaseModel):
    name: str = Field(
        examples=["dummy.pdf"], description="Name of the file including extension")
    account_id: int = Field(examples=[1], description="Selected account ID")
    file_type: str = DocumentType.STATEMENT.value


class DocumentToModel(DocumentRequest):
    # status: str = DocumentStatus.PENDING.value
    status: str = Field(default=DocumentStatus.PENDING.value, examples=[DocumentStatus.PENDING.value],
                        description="Document status")
    pass


class DocumentResponse(DocumentRequest):
    id: int
    file_type: Optional[str] = None
    status: Optional[str] = None
    sign_url: Optional[str] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class config:
        # orm_mode = True # pydantic version < 2.x
        from_attribute = True
