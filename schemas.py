import datetime
from pydantic import BaseModel, Field, field_validator


class TransactionBase(BaseModel):
    description: str
    amount: float = Field(title="Enter amount",
                          description="Amount here", gt=0, lt=1000)
    created_at: datetime.datetime
    # phone: Field(pattern=fr"\+880-\d{10}")

    @field_validator("amount")
    def verify_amount(cls, value):
        if value < 0:
            return ValueError("Amount should be grater than 0")
        return value


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int

    class config:
        # orm_mode = True # pydantic version < 2.x
        from_attribute = True
