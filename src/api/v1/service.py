from typing import Union, Optional

from fastapi import FastAPI

from instance_providers.client_providers import SpotifyClientProvider
from spotify.client import SpotifyClient

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/get_added_tracks/{offset}")
def read_item(offset: Optional[int] = None, q: Union[str, None] = None):
    spotify_client: SpotifyClient = SpotifyClientProvider().get_instance()
    return {"offset": offset, "items": spotify_client.get_liked_songs(offset=offset)}
