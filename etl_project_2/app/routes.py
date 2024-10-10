from fastapi import APIRouter, Depends, HTTPException
from .database import SessionLocal, load_data
from .models import Track, TrackCreate, TrackTable
import pandas as pd

router = APIRouter()

@router.post("/load_data_to_db/")
def load_data_to_db():
    """Endpoint to load data from CSV to the postgresql database."""
    df = pd.read_csv('C:/Users/sbyeo/MSDS/Data_Engineering/etl_project_2/data/cleaned_spotify_data.csv')
    session = SessionLocal()
    try:
        for index, row in df.iterrows():
            track = Track(
                track_name=row['track_name'],
                artist_name=row['artist(s)_name'],
                artist_count=row['artist_count'],
                released_year=row['released_year'],
                released_month=row['released_month'],
                released_day=row['released_day'],
                in_spotify_playlists=row['in_spotify_playlists'],
                streams=row['streams'],
                in_apple_playlists=row['in_apple_playlists'],
                in_deezer_playlists=row['in_deezer_playlists'],
                bpm=row['bpm'],
                key=row['key'],
                mode=row['mode'],
                danceability=row['danceability_%'] / 100,
                valence=row['valence_%'] / 100,
                energy=row['energy_%'] / 100,
                acousticness=row['acousticness_%'] / 100,
                instrumentalness=row['instrumentalness_%'] / 100,
                liveness=row['liveness_%'] / 100,
                speechiness=row['speechiness_%'] / 100,
                cover_url=row['cover_url'],
            )
            session.add(track)
        session.commit()
        return {"message": "Data loaded successfully"}
    except Exception as e:
        # Ensure the database remains consistent
        session.rollback()
        return {"error": str(e)}
    finally:
        session.close()

@router.get("/tracks/")
def get_tracks(skip: int = 0, limit: int = 10):
    """Endpoint to return all tracks with pagination."""
    df = load_data()
    tracks = df.iloc[skip:skip + limit].to_dict(orient="records")
    return tracks

@router.get("/tracks/{track_name}")
def get_track_by_name(track_name: str):
    """Endpoint to get a specific track by name.
    .str.contains(artist_name, case=False, na=False): This method checks each entry in the artist(s)_name column to see if it contains the string provided in the artist_name variable.
    case=False: This parameter makes the search case-insensitive, meaning it will match "latto", "Latto", or "LATTO" equally.
    na=False: This ensures that any NaN values in the artist(s)_name column are treated as False, preventing errors during the filtering process.
    track.to_dict(orient="records"): If there are matches, this converts the DataFrame to a list of dictionaries where each dictionary represents a row (track) in the DataFrame.
    orient="records" specifies that each row should be converted to a dictionary with column names as keys.
    """
    df = load_data()
    track = df[df['track_name'].str.contains(track_name, case=False, na=False)]
    return track.to_dict(orient="records") if not track.empty else {f"error: {track_name} not found"}

@router.get("/tracks/artist/{artist_name}")
def get_track_by_artist(artist_name: str):
    df = load_data()
    track = df[df["artist(s)_name"].str.contains(artist_name, case=False, na=False)]
    return track.to_dict(orient="records") if not track.empty else {f"error: No tracks found for the {artist_name}."}

@router.post("/tracks/", response_model=Track)
def create_track(new_track: TrackCreate):
    """Endpoint to create a new track in the database."""
    session = SessionLocal()
    try:
        track = TrackTable(  # Creating an instance of the ORM model
            track_name=new_track.track_name,
            artist_name=new_track.artist_name,
            artist_count=new_track.artist_count,
            released_year=new_track.released_year,
            released_month=new_track.released_month,
            released_day=new_track.released_day,
            in_spotify_playlists=new_track.in_spotify_playlists,
            streams=new_track.streams,
            in_apple_playlists=new_track.in_apple_playlists,
            in_deezer_playlists=new_track.in_deezer_playlists,
            bpm=new_track.bpm,
            key=new_track.key,
            mode=new_track.mode,
            danceability=new_track.danceability,
            valence=new_track.valence,
            energy=new_track.energy,
            acousticness=new_track.acousticness,
            instrumentalness=new_track.instrumentalness,
            liveness=new_track.liveness,
            speechiness=new_track.speechiness,
            cover_url=new_track.cover_url,
        )
        session.add(track)
        session.commit()
        session.refresh(track)
        return track
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create track: {str(e)}")
    finally:
        session.close()


@router.delete("/tracks/{track_id}", response_model=dict)
def delete_track(track_id: int):
    """Endpoint to delete a track by its ID."""
    session = SessionLocal()
    try:
        # Query the track by its ID
        track = session.query(TrackTable).filter(TrackTable.id == track_id).first()

        # Check if the track exists
        if not track:
            raise HTTPException(status_code=404, detail="Track not found")

        session.delete(track)  # Delete the track from the session
        session.commit()  # Commit the transaction
        return {"message": "Track deleted successfully"}

    except Exception as e:
        session.rollback()  # Rollback on error
        raise HTTPException(status_code=500, detail=f"Failed to delete track: {str(e)}")

    finally:
        session.close()  # Close the session