import pathlib
from configparser import ConfigParser

PATH = pathlib.Path(__file__).parent.absolute()
CONFIG_FILE_NAME = 'config.ini'
CONFIG_FULL_PATH = PATH / CONFIG_FILE_NAME
CONFIG_SECTION = "DEFAULT"
CONFIG_SPOTIFY_CREDENTIALS_FILE_NAME_KEY = "SpotifyClientCredentialsLocation"

config = ConfigParser()
config.read(CONFIG_FULL_PATH)