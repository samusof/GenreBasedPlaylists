import configparser
from configparser import ConfigParser
import json
from json import JSONDecodeError

import spotipy

from src.app_logging.logger import logger
from spotipy.oauth2 import SpotifyOAuth

from src.config import CONFIG_SECTION, CONFIG_SPOTIFY_CREDENTIALS_FILE_NAME_KEY

CLIENT_ID_KEY = 'client_id'
CLIENT_SECRET_KEY = 'client_secret'


class SpotifyApiCredentialLoader:
    _client_id: str
    _client_secret: str

    def __init__(self, config: ConfigParser):
        self._populate_credentials(config)

    def _get_spotify_credentials_file_data_from_config(self, config: ConfigParser) -> dict:
        try:
            credential_file_name: str = config.get(CONFIG_SECTION, CONFIG_SPOTIFY_CREDENTIALS_FILE_NAME_KEY)
            try:
                with open(credential_file_name, 'r') as creds_file:
                    try:
                        creds_json: json = json.loads(creds_file.read())
                        return creds_json
                    except JSONDecodeError as jde:
                        logger.error('Credential file not in json format')
                        raise jde
            except IOError as ioe:
                logger.error("No Spotify credentials file found at {}".format(credential_file_name))
                raise ioe
        except configparser.NoOptionError as noe:
            logger.error('{} not set in config file'.format(CONFIG_SPOTIFY_CREDENTIALS_FILE_NAME_KEY))
            raise noe

    def _populate_credentials(self, config: ConfigParser) -> None:
        creds_json: dict = self._get_spotify_credentials_file_data_from_config(config)
        try:
            self._client_id = creds_json[CLIENT_ID_KEY]
            self._client_secret = creds_json[CLIENT_SECRET_KEY]
        except KeyError as ke:
            logger.error("Spotify credentials file is missing some credentials.")
            raise ke

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

    def __init__(self, spotify_credential_loader: SpotifyApiCredentialLoader):
        self._credential_loader = spotify_credential_loader
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
        self._client_id = self._credential_loader.get_client_id()
        self._client_secret = self._credential_loader.get_client_secret()

    def get_liked_songs(self):
        tracks_raw: dict = self._spotify_api.current_user_saved_tracks(limit=50)
        # with open('out.json', 'w') as file:
        #     file.write(str(tracks_raw))
        tracks = [x['track']['name'] for x in tracks_raw['items']]
        for track in tracks:
            logger.info(track)
