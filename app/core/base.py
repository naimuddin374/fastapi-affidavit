from sqlalchemy.ext.declarative import declarative_base

# Defining Base here prevents circular imports between db.py and models.py
Base = declarative_base()
