from typing import Optional

from pydantic import BaseModel


class CarBase(BaseModel):
  make: str
  model: str
  year: int
  body_type: Optional[str] = None
  engine_volume: Optional[float] = None
  horsepower: Optional[int] = None


class CarCreate(CarBase):
  pass


class Car(CarBase):
  id: int

  class Config:
    orm_mode = True
