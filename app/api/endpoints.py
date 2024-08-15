# app/api/endpoints.py

import logging
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import auth

from .. import crud, models, schemas
from ..database import get_db

logger = logging.getLogger("default")
router = APIRouter()


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
  user = db.query(models.User).filter(models.User.username == form_data.username).first()
  if not user or not auth.verify_password(form_data.password, user.hashed_password):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
  access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = auth.create_access_token(
      data={"sub": user.username}, expires_delta=access_token_expires
  )
  return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
  db_user = crud.create_user_query(user, db)
  if not db_user:
    raise HTTPException(status_code=400, detail="Email already registered")
  return db_user


@router.get("/car_info", response_model=list[schemas.Car])
def get_car_info(model: str, db: Session = Depends(get_db)):
  car = crud.get_cars_by_model_query(db, model=model)
  if not car:
    raise HTTPException(status_code=404, detail="Car not found")
  return car


@router.post("/car_info", response_model=schemas.Car)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
  try:
    car_obj = crud.create_car_query(db=db, car=car)
    logger.info(f"USER: {current_user.username} created car with ID: {car_obj.id}")
    return car_obj
  except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/car_info/{car_id}", response_model=schemas.Car)
def update_car(car_id: int, car: schemas.CarCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
  updated_car = crud.update_car_query(db=db, car_id=car_id, car=car)
  if not updated_car:
    raise HTTPException(status_code=404, detail="Car not found")

  logger.info(f"USER: {current_user.username} updated car with ID: {updated_car.id}")
  return updated_car


@router.get("/car_info/", response_model=list[schemas.Car])
def filter_cars(
    year: Optional[int] = Query(None, description="Filter by year of manufacture"),
    body_type: Optional[str] = Query(None, description="Filter by body type"),
    db: Session = Depends(get_db)
):
  cars = crud.get_cars_by_filters_query(db, year, body_type)
  if not cars:
    raise HTTPException(status_code=404, detail="No cars found matching the criteria")
  return cars
