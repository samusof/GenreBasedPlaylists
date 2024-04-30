from enum import Enum
from typing import List, Optional
from spotipy import Spotify
from spotify.models import SpotifyAddedTrack


class SpotifyWebApiScope(str, Enum):
    USER_LIBRARY_READ = 'user-library-read'


class SpotifyWebApiScopeBuilder:
    @staticmethod
    def build_scope_param(scopes: List[SpotifyWebApiScope]) -> str:
        return " ".join(scopes)


class SpotifyClient:
    _spotipy_client: Spotify

    def __init__(self, spotipy_client: Spotify):
        self._spotipy_client = spotipy_client

    def get_liked_songs(self, offset: Optional[int] = None) -> List[SpotifyAddedTrack]:
        tracks_raw: dict = self._spotipy_client.current_user_saved_tracks(limit=50, offset=offset)
        added_tracks: List[SpotifyAddedTrack] = [SpotifyAddedTrack(**x) for x in tracks_raw['items']]
        return added_tracks
