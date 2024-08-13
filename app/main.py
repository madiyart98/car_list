# app/main.py

from fastapi import FastAPI
from .api import endpoints
from .database import engine
from .models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(endpoints.router)
