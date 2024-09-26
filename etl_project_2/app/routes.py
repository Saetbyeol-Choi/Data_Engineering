from fastapi import APIRouter, Depends
from .database import SessionLocal, load_data
from .models import Track
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


# # Update a Track
# @router.put("/tracks/{track_id}")
# def update_track(track_id: int, track: Track):
#     """Endpoint to update a track record."""
#     session = SessionLocal()
#     try:
#         existing_track = session.query(Track).filter(Track.id == track_id).first()
#         if not existing_track:
#             return {"error": "Track not found."}
#
#         for key, value in track.dict().items():
#             setattr(existing_track, key, value)
#
#         session.commit()
#         return {"message": "Track updated successfully."}
#     except Exception as e:
#         session.rollback()
#         return {"error": str(e)}
#     finally:
#         session.close()
#
# # Delete a Track
# @router.delete("/tracks/{track_id}")
# def delete_track(track_id: int):
#     """Endpoint to delete a track."""
#     session = SessionLocal()
#     try:
#         track = session.query(Track).filter(Track.id == track_id).first()
#         if not track:
#             return {"error": "Track not found."}
#
#         session.delete(track)
#         session.commit()
#         return {"message": "Track deleted successfully."}
#     except Exception as e:
#         session.rollback()
#         return {"error": str(e)}
#     finally:
#         session.close()
#
# # Provide Statistics
# @router.get("/tracks/stats/")
# def get_tracks_statistics():
#     """Endpoint to get statistics about the dataset."""
#     df = load_data()
#     total_tracks = len(df)
#     total_streams = df['streams'].sum()
#     average_energy = df['energy_%'].mean()
#
#     return {
#         "total_tracks": total_tracks,
#         "total_streams": total_streams,
#         "average_energy": average_energy
#     }

