import pytest
from configparser import ConfigParser

TEST_CREDENTIALS_FILE_NAME = 'someFile.json'


def valid_config() -> ConfigParser:
    config = ConfigParser()
    config.set(section="DEFAULT", option="SpotifyClientCredentialsLocation", value=TEST_CREDENTIALS_FILE_NAME)
    return config


def invalid_config() -> ConfigParser:
    config = ConfigParser()
    config.remove_option(section="DEFAULT", option="SpotifyClientCredentialsLocation")
    return config


@pytest.fixture(scope="class")
def mock_config(request):
    request.cls.config = valid_config()


@pytest.fixture(scope="class")
def mock_malformed_config(request):
    request.cls.malformed_config = invalid_config()
