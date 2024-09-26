from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pandas as pd

DATABASE_URL = 'postgresql://postgres:12345!@localhost:5432/music_db'  # Update with your DB details

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def load_data():
    df = pd.read_csv('data/cleaned_spotify_data.csv')
    return df