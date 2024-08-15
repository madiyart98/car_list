import os

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


class Settings:
  DATABASE_NAME: str = os.getenv("DATABASE_NAME", "car_info")
  DATABASE_USER: str = os.getenv("DATABASE_USER", "postgres")
  DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "password")
  DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
  DATABASE_PORT: str = os.getenv("DATABASE_PORT", "5432")
  DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
  DATABASE_URL = f'postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
  TOKEN_VERIFICATION_KEY: str = os.getenv("TOKEN_VERIFICATION_KEY", "")


settings = Settings()
