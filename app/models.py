# models.py
from sqlalchemy import Boolean, Column, Float, Integer, String

from app.database import Base


class Car(Base):
  __tablename__ = 'cars'

  id = Column(Integer, primary_key=True, index=True)
  mark = Column(String, index=True)
  model = Column(String, index=True)
  year = Column(Integer)
  body_type = Column(String)
  engine_volume = Column(Float)
  horsepower = Column(Integer)


class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, index=True)
  email = Column(String, unique=True, index=True)
  hashed_password = Column(String)
  is_active = Column(Boolean, default=True)
