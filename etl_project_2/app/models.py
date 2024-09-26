from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Track(Base):
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
