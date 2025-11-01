from sqlalchemy.orm import declarative_base
from app.core.base import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    account_id = Column(Integer)
    amount = Column(Float(2))
    created_at = Column(DateTime)


class History(Base):
    __tablename__ = 'histories'

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer)
    created_at = Column(DateTime)


class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer)
    name = Column(String)
    path = Column(String)
    created_at = Column(DateTime)
