import datetime
from pydantic import BaseModel
from typing import Optional


class DocumentBase(BaseModel):
    account_id: int
    name: str
    path: str
    # path: Optional[str]
    created_at: datetime.datetime
    # phone: Field(pattern=fr"\+880-\d{10}")


class DocumentCreate(DocumentBase):
    pass


class Document(DocumentBase):
    id: int

    class config:
        # orm_mode = True # pydantic version < 2.x
        from_attribute = True
