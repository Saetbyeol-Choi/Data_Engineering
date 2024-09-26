import pytest
from fastapi.testclient import TestClient
from .main import app
from .database import load_data

client = TestClient(app) # to simulate requests to API
"""The client is an instance of TestClient from fastapi.testclient, which allows you to make requests to your API without needing to run the server.
"""

def test_get_tracks():
    print("Endpoint Test_1: get_tracks")
    response = client.get("/tracks/?skip=0&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    """ 
    isinstance is used for type checking, allowing developers to confirm the type of an object at runtime
    """
    assert len(response.json()) <= 10
    print("get_tracks test passed!\n")

def test_get_track_by_name():
    print("Endpoint Test_2: get_track_by_name")
    # Test for an existing track
    df = load_data()
    existing_track_name = df['track_name'].iloc[0].strip().split()[0]  # Get the first existing track name
    print(f"Searching for track: {existing_track_name}")

    response = client.get(f"/tracks/{existing_track_name}")
    response_json = response.json()
    print(f"Response JSON: {response_json}\n")
    assert response.status_code == 200
    assert isinstance(response_json, list) and len(response_json) > 0
    assert response_json[0]["track_name"].startswith(existing_track_name)

    # Test for a non-existing track
    track_name = "non-existing-track"
    response = client.get(f"/tracks/{track_name}")
    assert response.status_code == 200
    assert response.json() == [f"error: {track_name} not found"]
    print("Non-existing track test passed!\n")

def test_get_track_by_artist():
    print("Endpoint Test_3: get_track_by_artist")

    # Test for an existing artist
    df = load_data()
    existing_artist_name = df['artist(s)_name'].iloc[0]  # Get the first existing artist name
    print(f"Searching for artist: {existing_artist_name}")

    response = client.get(f"/tracks/artist/{existing_artist_name}")
    response_json = response.json()
    print(f"Response JSON: {response_json}\n")
    assert response.status_code == 200
    assert isinstance(response_json, list) and len(response_json) > 0
    assert response_json[0]["artist(s)_name"] == existing_artist_name

    # Test for a non-existing artist
    artist_name = "non-existing-artist"
    response = client.get(f"/tracks/artist/{artist_name}")
    assert response.status_code == 200
    assert response.json() == [f"error: No tracks found for the {artist_name}."]
    print("Non-existing artist test passed!\n")


if __name__ == "__main__":
    pytest.main()
