import csv

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Car


def load_csv_data(file_path: str, db: Session):
  with open(file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
      # Convert numeric fields
      engine_volume = float(row['engine_volume']) if row['engine_volume'].lower() != 'electric' else None
      horsepower = int(row['horsepower']) if row['horsepower'] else None

      car = Car(
          id=int(row['id']),
          mark=row['mark'],
          model=row['model'],
          year=int(row['year']),
          body_type=row['body_type'],
          engine_volume=engine_volume,
          horsepower=horsepower
      )
      db.add(car)
    db.commit()


if __name__ == "__main__":
  db = SessionLocal()
  try:
    load_csv_data('cars.csv', db)
  finally:
    db.close()
