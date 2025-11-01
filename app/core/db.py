import app.models.models
import os
from dotenv import load_dotenv
from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.base import Base

load_dotenv()


DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker[Session](
    autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_table():
    Base.metadata.create_all(engine)
    print("Table sync successfully")

# create_table()
