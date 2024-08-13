# app/main.py

from fastapi import FastAPI

from app.core.logging_config import setup_logging

from .api import endpoints
from .database import engine
from .models import Base

setup_logging()
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(endpoints.router)
