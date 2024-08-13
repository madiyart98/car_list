# app/api/endpoints.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()


@router.get("/car_info", response_model=schemas.Car)
def get_car_info(model: str, db: Session = Depends(get_db)):
  car = crud.get_car_by_model(db, model=model)
  if not car:
    raise HTTPException(status_code=404, detail="Car not found")
  return car


@router.post("/car_info", response_model=schemas.Car)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
  return crud.create_car(db=db, car=car)


@router.put("/car_info/{car_id}", response_model=schemas.Car)
def update_car(car_id: int, car: schemas.CarCreate, db: Session = Depends(get_db)):
  updated_car = crud.update_car(db=db, car_id=car_id, car=car)
  if not updated_car:
    raise HTTPException(status_code=404, detail="Car not found")
  return updated_car
