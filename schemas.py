import datetime
from pydantic import BaseModel


class TransactionBase(BaseModel):
    description: str
    amount: float
    created_at: datetime.datetime


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int

    class config:
        # orm_mode = True # pydantic version < 2.x
        from_attribute = True
