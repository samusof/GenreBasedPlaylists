import configparser
from configparser import ConfigParser
import json
from json import JSONDecodeError

from app_logging.logger import logger
from constants import CLIENT_ID_KEY, CLIENT_SECRET_KEY
from src.config import CONFIG_SECTION, CONFIG_SPOTIFY_CREDENTIALS_FILE_NAME_KEY


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
