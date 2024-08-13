# app/crud.py

from sqlalchemy import or_
from sqlalchemy.orm import Session

from . import models, schemas


def get_cars_by_model(db: Session, model: str):
  return db.query(models.Car).filter(
      or_(
          models.Car.model.ilike(f'%{model}%'),
          models.Car.mark.ilike(f'%{model}%')
      )
  ).all()


def get_cars_by_filters(db: Session, year: int | None = None, body_type: str | None = None):
  query = db.query(models.Car)

  if year is not None:
    query = query.filter(models.Car.year == year)

  if body_type is not None:
    query = query.filter(models.Car.body_type.ilike(f'%{body_type}%'))

  return query.all()


def create_car(db: Session, car: schemas.CarCreate):
  db_car = models.Car(**car.dict())
  db.add(db_car)
  db.commit()
  db.refresh(db_car)
  return db_car


def update_car(db: Session, car_id: int, car: schemas.CarCreate):
  db_car = db.query(models.Car).filter(models.Car.id == car_id).first()
  if db_car:
    for key, value in car.dict().items():
      setattr(db_car, key, value)
    db.commit()
    db.refresh(db_car)
  return db_car
