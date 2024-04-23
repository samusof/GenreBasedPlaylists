from configparser import ConfigParser
import json
import spotipy

from app_logging.logger import logger
from spotipy.oauth2 import SpotifyOAuth


class SpotifyApiCredentialLoader:
    _client_id: str
    _client_secret: str

    def __init__(self, config: ConfigParser):
        self._populate_credentials(config)

    def _populate_credentials(self, config: ConfigParser) -> None:
        credential_file_name = config.get("DEFAULT", "SpotifyClientCredentialsLocation")
        with open(credential_file_name, 'r') as creds:
            creds_json: json = json.loads(creds.read())
            self._client_id = creds_json["client_id"]
            self._client_secret = creds_json["client_secret"]

    def get_client_id(self) -> str:
        return self._client_id

    def get_client_secret(self) -> str:
        return self._client_secret


class SpotifyApi:

    _client_id: str
    _client_secret: str
    _redirect_uri: str
    _scope: str
    _spotify_api: spotipy.Spotify
    _credential_loader: SpotifyApiCredentialLoader

    def __init__(self, config: ConfigParser):
        self._credential_loader = SpotifyApiCredentialLoader(config)
        self._populate_credentials()
        self._redirect_uri = 'http://localhost:3000'
        self._scope = 'user-library-read'
        self._authorise()

    def _authorise(self):
        logger.info("authorising using user: {} and pass: {}".format(self._client_id, "*" * len(self._client_secret)))
        self._spotify_api = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self._client_id,
            client_secret=self._client_secret,
            redirect_uri=self._redirect_uri,
            scope=self._scope))

    def _populate_credentials(self):
        # logger.info("reading credentials from file: {}".format(file_name))
        self._client_id = self._credential_loader.get_client_id()
        self._client_secret = self._credential_loader.get_client_secret()

    def get_liked_songs(self):
        tracks_raw: dict = self._spotify_api.current_user_saved_tracks(limit=50)
        # with open('out.json', 'w') as file:
        #     file.write(str(tracks_raw))
        tracks = [x['track']['name'] for x in tracks_raw['items']]
        for track in tracks:
            logger.info(track)
