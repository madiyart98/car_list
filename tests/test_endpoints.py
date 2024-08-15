import logging
from venv import logger

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

logger = logging.getLogger(__name__)
# Create a test database engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database


def override_get_db():
  try:
    db = TestingSessionLocal()
    yield db
  finally:
    db.close()


app.dependency_overrides[get_db] = override_get_db

# Create the test client
client = TestClient(app, base_url="http://localhost:8000")

# Create the database schema
Base.metadata.create_all(bind=engine)

# The cleanup_database fixture is automatically applied


@pytest.fixture(scope="session", autouse=True)
def cleanup_database():
  yield
  Base.metadata.drop_all(bind=engine)


def authenticate_test_user():
  response = client.post(
      "/token",
      data={"username": "testuser", "password": "Testpassword1_4"},
  )
  return response.json()["access_token"]


def test_register_user():
  response = client.post(
      "/users/",
      json={"username": "testuser", "email": "test@example.com", "password": "Testpassword1_4"},
  )
  print(response.json())
  assert response.status_code == 200
  assert response.json()["email"] == "test@example.com"


def test_login_for_access_token():
  # Register a user first
  # client.post(
  #     "/users/",
  #     json={"username": "testuser", "email": "test@example.com", "password": "Testpassword1_4"},
  # )
  response = client.post(
      "/token",
      data={"username": "testuser", "password": "Testpassword1_4"},
  )
  assert response.status_code == 200
  assert "access_token" in response.json()


def test_create_car():
  response = client.post(
      "/car_info",
      json={"mark": "Toyota", "model": "Camry", "year": 2021, "body_type": "Sedan", "engine_volume": 2.5, "horsepower": 203},
  )
  assert response.status_code == 401
  token = authenticate_test_user()
  response = client.post(
      "/car_info",
      json={"mark": "Toyota", "model": "Camry", "year": 2021, "body_type": "Sedan", "engine_volume": 2.5, "horsepower": 203},
      headers={"Authorization": f"Bearer {token}"}
  )
  assert response.status_code == 200
  assert response.json()["model"] == "Camry"


def test_get_car_info():
  response = client.get("/car_info", params={"model": "Camry"})
  assert response.status_code == 200
  assert response.json()[0]["model"] == "Camry"

  response = client.get("/car_info", params={"model": "Honda"})
  assert response.status_code == 404


def test_update_car():
  # Create a car first
  token = authenticate_test_user()
  create_response = client.post(
      "/car_info",
      json={"mark": "Honda", "model": "Civic", "year": 2019, "body_type": "Coupe", "engine_volume": 1.5, "horsepower": 174},
      headers={"Authorization": f"Bearer {token}"}
  )
  car_id = create_response.json()["id"]
  # Update the car
  update_response = client.put(
      f"/car_info/{car_id}",
      json={"mark": "Honda", "model": "Civic", "year": 2020, "body_type": "Coupe", "engine_volume": 1.5, "horsepower": 180},
      headers={"Authorization": f"Bearer {token}"}
  )
  assert update_response.status_code == 200
  assert update_response.json()["year"] == 2020

  update_response = client.put(
      f"/car_info/{car_id}",
      json={"mark": "Honda", "model": "Civic", "year": 2020, "body_type": "Coupe", "engine_volume": 1.5, "horsepower": 180},
  )
  assert update_response.status_code == 401


def test_filter_cars():
  # Create cars first
  token = authenticate_test_user()

  client.post(
      "/car_info",
      json={"mark": "Mazda", "model": "3", "year": 2025, "body_type": "Hatchback", "engine_volume": 2.0, "horsepower": 155},
      headers={"Authorization": f"Bearer {token}"}
  )
  client.post(
      "/car_info",
      json={"mark": "Mazda", "model": "6", "year": 2020, "body_type": "Sedan", "engine_volume": 2.5, "horsepower": 187},
      headers={"Authorization": f"Bearer {token}"}
  )
  response = client.get("/car_info/", params={"year": 2025})
  assert response.status_code == 200
  assert len(response.json()) == 1
  assert response.json()[0]["year"] == 2025
