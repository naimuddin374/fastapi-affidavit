from datetime import datetime
from app.core.base import Base
from sqlalchemy import Enum, Column, ForeignKey, Integer, String, Float, DateTime
from app.types.system_types import DocumentStatus, DocumentType


class TransactionModel(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    account_id = Column(Integer)
    amount = Column(Float(2))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        # This string will be printed when you use 'print(instance)'
        # We include the ID and a descriptive field like file_name
        return (f"  , \n"
                f"id={self.id}, \n"
                f"description={self.description}, \n"
                f"account_id='{self.account_id}', \n"
                f"amount='{self.amount}', \n"
                f"status='{self.status}', \n"
                f"created_at='{self.created_at}', \n"
                f"updated_at='{self.updated_at}', \n"
                f"' \n")


class DocumentModel(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer)
    name = Column(String)
    file_type = Column(String(50),
                       default=DocumentType.STATEMENT.value, nullable=False)
    status = Column(String(50),
                    default=DocumentStatus.PENDING.value, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        # This string will be printed when you use 'print(instance)'
        # We include the ID and a descriptive field like file_name
        return (f"  , \n"
                f"id={self.id}, \n"
                f"account_id={self.account_id}, \n"
                f"name='{self.name}', \n"
                f"file_type='{self.file_type}', \n"
                f"status='{self.status}', \n"
                f"created_at='{self.created_at}', \n"
                f"updated_at='{self.updated_at}', \n"
                f"' \n")
