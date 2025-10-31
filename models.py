from db import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    amount = Column(Float(2))
    created_at = Column(DateTime)


class Histories(Base):
    __tablename__ = 'histories'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
