from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pandas as pd
import os

DATABASE_URL = 'postgresql://postgres:12345!@localhost:5432/music_db'  # Update with your DB details

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

CSV_PATH = os.getenv('CSV_PATH', 'data/cleaned_spotify_data.csv')  # Default path if not set

def load_data():
    df = pd.read_csv(CSV_PATH)
    return df