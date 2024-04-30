from unittest.mock import Mock

import pytest
from configparser import ConfigParser

from spotify.credential_provider import SpotifyApiCredentialLoader

TEST_CREDENTIALS_FILE_NAME = 'someFile.json'


def valid_config() -> ConfigParser:
    config = ConfigParser()
    config.set(section="DEFAULT", option="SpotifyClientCredentialsLocation", value=TEST_CREDENTIALS_FILE_NAME)
    return config


def invalid_config() -> ConfigParser:
    config = ConfigParser()
    config.remove_option(section="DEFAULT", option="SpotifyClientCredentialsLocation")
    return config


def valid_creds_loader() -> SpotifyApiCredentialLoader:
    creds_loader = Mock()
    creds_loader.get_client_id = Mock()
    creds_loader.get_client_secret = Mock()
    creds_loader.get_client_id.return_value = "valid_client_id"
    creds_loader.get_client_secret.return_value = "valid_client_secret"
    return creds_loader


@pytest.fixture(scope="class")
def mock_config(request):
    request.cls.config = valid_config()


@pytest.fixture(scope="class")
def mock_malformed_config(request):
    request.cls.malformed_config = invalid_config()


@pytest.fixture(scope="class")
def mock_spotify_api_creds_loader(request):
    request.cls.spotify_api_creds_loader = valid_creds_loader()
