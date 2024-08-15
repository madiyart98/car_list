# app/crud.py

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.auth import auth

from . import models, schemas


def create_user_query(user: schemas.UserCreate, db: Session) -> models.User | None:
  db_user = db.query(models.User).filter(models.User.email == user.email).first()
  if db_user:
    return None
  hashed_password = auth.get_password_hash(user.password)
  db_user = models.User(
      username=user.username,
      email=user.email,
      hashed_password=hashed_password,
  )
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user


def get_cars_by_model_query(db: Session, model: str):
  return db.query(models.Car).filter(
      or_(
          models.Car.model.ilike(f'%{model}%'),
          models.Car.mark.ilike(f'%{model}%')
      )
  ).all()


def get_cars_by_filters_query(db: Session, year: int | None = None, body_type: str | None = None):
  query = db.query(models.Car)

  if year is not None:
    query = query.filter(models.Car.year == year)

  if body_type is not None:
    query = query.filter(models.Car.body_type.ilike(f'%{body_type}%'))

  return query.all()


def create_car_query(db: Session, car: schemas.CarCreate):
  db_car = models.Car(**car.model_dump())
  db.add(db_car)
  db.commit()
  db.refresh(db_car)
  return db_car


def update_car_query(db: Session, car_id: int, car: schemas.CarCreate):
  db_car = db.query(models.Car).filter(models.Car.id == car_id).first()
  if db_car:
    for key, value in car.model_dump().items():
      setattr(db_car, key, value)
    db.commit()
    db.refresh(db_car)
  return db_car
