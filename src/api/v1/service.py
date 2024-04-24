from typing import Union

from fastapi import FastAPI

from spotify.client import SpotifyApi, SpotifyClient

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/last_added_tracks/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    spotify_client: SpotifyApi = SpotifyClient().get_client()
    return {"item_id": item_id, "q": q, "items": spotify_client.get_liked_songs()}