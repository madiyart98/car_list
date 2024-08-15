from typing import Optional

from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
  access_token: str
  token_type: str


class TokenData(BaseModel):
  username: str


class UserBase(BaseModel):
  username: str
  email: str


class UserCreate(UserBase):
  password: str


class User(UserBase):
  id: int
  is_active: bool

  # Use ConfigDict and set from_attributes for ORM compatibility
  model_config = ConfigDict(from_attributes=True)


class CarBase(BaseModel):
  mark: str
  model: str
  year: int
  body_type: Optional[str] = None
  engine_volume: Optional[float] = None
  horsepower: Optional[int] = None


class CarCreate(CarBase):
  pass


class Car(CarBase):
  id: int

  # Use ConfigDict and set from_attributes for ORM compatibility
  model_config = ConfigDict(from_attributes=True)
