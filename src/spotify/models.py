from datetime import datetime
from enum import Enum
from typing import List, Union

from pydantic import BaseModel


class SpotifyArtist(BaseModel):
    name: str
    id: str


class SpotifyGenreAwareArtist(SpotifyArtist):
    genres: List[str]


class SpotifyAlbumType(str, Enum):
    SINGLE = 'single'
    ALBUM = 'album'
    COMPILATION = 'compilation'


class SpotifySingle(BaseModel):
    album_type: SpotifyAlbumType


class SpotifyAlbum(BaseModel):
    album_type: SpotifyAlbumType
    artists: List[SpotifyArtist]
    name: str
    id: str


class SpotifyTrack(BaseModel):
    artists: List[SpotifyArtist]
    album: Union[SpotifyAlbum, SpotifySingle]
    name: str
    id: str


class SpotifyAddedTrack(BaseModel):
    added_at: datetime
    track: SpotifyTrack
