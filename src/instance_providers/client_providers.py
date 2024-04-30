from typing import Optional, Generic, TypeVar

from spotipy import Spotify, SpotifyOAuth

from app_logging.logger import logger
from config import config
from constants import SPOTIFY_REDIRECT_URI
from instance_providers.singleton import Singleton
from spotify.client import SpotifyClient, SpotifyWebApiScopeBuilder, SpotifyWebApiScope
from spotify.credential_provider import SpotifyApiCredentialLoader

T = TypeVar("T")


class InstanceProvider(Generic[T], metaclass=Singleton):
    _instance = Optional[T]

    def __init__(self):
        self._instance = None

    def get_instance(self) -> T:
        if self._instance is None:
            self._initialise_instance()
        return self._instance

    def _initialise_instance(self) -> None:
        pass


class SpotifyApiCredentialLoaderProvider(InstanceProvider[SpotifyApiCredentialLoader]):
    def _initialise_instance(self):
        self._instance = SpotifyApiCredentialLoader(config)


class SpotipyClientProvider(InstanceProvider[Spotify]):
    def _initialise_instance(self):
        creds_loader = SpotifyApiCredentialLoaderProvider().get_instance()
        client_id = creds_loader.get_client_id()
        client_secret = creds_loader.get_client_secret()
        scope = SpotifyWebApiScopeBuilder.build_scope_param([SpotifyWebApiScope.USER_LIBRARY_READ])
        redirect_uri = SPOTIFY_REDIRECT_URI
        logger.info("authorising using user: {} and pass: {}".format(client_id, "*" * 4))
        spotipy_api_client = Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope))
        self._instance = spotipy_api_client


class SpotifyClientProvider(InstanceProvider[SpotifyClient]):
    def _initialise_instance(self):
        spotipy_client = SpotipyClientProvider().get_instance()
        self._instance = SpotifyClient(spotipy_client)
