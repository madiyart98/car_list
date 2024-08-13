import os

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


class Settings:
  DATABASE_NAME: str = os.getenv("DATABASE_NAME", "car_info")
  DATABASE_USER: str = os.getenv("DATABASE_USER", "postgres")
  DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "password")
  DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
  DATABASE_PORT: str = os.getenv("DATABASE_PORT", "postgres")
  DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
  DATABASE_URL = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}:{DATABASE_PORT}'


settings = Settings()
