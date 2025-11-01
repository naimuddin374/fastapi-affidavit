import datetime
from pydantic import BaseModel
from typing import Optional


class DocumentBase(BaseModel):
    name: str
    account_id: int
    created_at: Optional[datetime.datetime] = None
    # phone: Field(pattern=fr"\+880-\d{10}")


class DocumentCreate(DocumentBase):
    created_at: Optional[datetime.datetime] = None
    pass


class DocumentRead(DocumentBase):
    id: int
    created_at: datetime.datetime
    sign_url: Optional[str] = None

    class config:
        # orm_mode = True # pydantic version < 2.x
        from_attribute = True
