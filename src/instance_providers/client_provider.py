from typing import Optional

from config import config
from instance_providers.singleton import Singleton
from spotify.client import SpotifyClient, SpotifyApiCredentialLoader


class SpotifyClientProvider(metaclass=Singleton):
    _client: Optional[SpotifyClient]

    def __init__(self):
        self._client = None

    def get_client(self) -> SpotifyClient:
        if self._client is not None:
            return self._client
        else:
            credential_loader = SpotifyApiCredentialLoader(config)
            return SpotifyClient(credential_loader)
