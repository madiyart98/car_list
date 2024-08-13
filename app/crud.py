# app/crud.py

from sqlalchemy.orm import Session

from . import models, schemas


def get_car_by_model(db: Session, model: str):
  return db.query(models.Car).filter(models.Car.model == model).first()


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
