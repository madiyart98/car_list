# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base  # Update this line
from sqlalchemy.orm import sessionmaker

from .core.config import settings

Base = declarative_base()
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
