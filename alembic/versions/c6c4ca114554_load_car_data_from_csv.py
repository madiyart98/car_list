"""Load car data from CSV

Revision ID: c6c4ca114554
Revises: 9bb38d7b4207
Create Date: 2024-08-13 21:43:30.625041

"""
import csv
import os
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.orm import Session

from alembic import op
from app.database import Base
# Import your Car model
from app.models import Car

# revision identifiers, used by Alembic.
revision: str = 'c6c4ca114554'
down_revision: Union[str, None] = '9bb38d7b4207'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def load_csv_data(session: Session, file_path: str):
  with open(file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
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
      session.add(car)
    session.commit()


def upgrade():
  # Bind the session to the current context
  bind = op.get_bind()
  session = Session(bind=bind)

  # Specify the path to your CSV file
  base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
  csv_file_path = os.path.join(base_dir, 'cars.csv')

  # Load the data from the CSV file
  load_csv_data(session, csv_file_path)


def downgrade():
  # In case of downgrade, you can remove the inserted data
  bind = op.get_bind()
  session = Session(bind=bind)

  session.query(Car).delete()
  session.commit()
