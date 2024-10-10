from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from pydantic import BaseModel

class TrackTable(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    track_name = Column(String, nullable=False)
    artist_name = Column(String, nullable=False)
    artist_count = Column(Integer)
    released_year = Column(Integer)
    released_month = Column(Integer)
    released_day = Column(Integer)
    in_spotify_playlists = Column(Integer)
    streams = Column(Float)
    in_apple_playlists = Column(Integer)
    in_deezer_playlists = Column(Integer)
    bpm = Column(Integer)
    key = Column(String)
    mode = Column(String)
    danceability = Column(Integer)
    valence = Column(Integer)
    energy = Column(Integer)
    acousticness = Column(Integer)
    instrumentalness = Column(Integer)
    liveness = Column(Integer)
    speechiness = Column(Integer)
    cover_url = Column(String)

class TrackBase(BaseModel):
    track_name: str
    artist_name: str
    artist_count: int
    released_year: int
    released_month: int
    released_day: int
    in_spotify_playlists: int
    streams: float
    in_apple_playlists: int
    in_deezer_playlists: int
    bpm: int
    key: str
    mode: str
    danceability: float
    valence: float
    energy: float
    acousticness: float
    instrumentalness: float
    liveness: float
    speechiness: float
    cover_url: str

class TrackCreate(TrackBase):
    pass

class Track(TrackBase):
    id: int

    # Allow the model to read data from SQLAlchemy ORM models
    class Config:
        orm_mode = True