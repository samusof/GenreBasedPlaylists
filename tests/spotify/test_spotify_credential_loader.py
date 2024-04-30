import configparser
import json
from json import JSONDecodeError

from src.config import CONFIG_SECTION, CONFIG_SPOTIFY_CREDENTIALS_FILE_NAME_KEY
from src.spotify.credential_provider import SpotifyApiCredentialLoader
import unittest
import unittest.mock as mock
import pytest
from src.spotify.credential_provider import CLIENT_SECRET_KEY, CLIENT_ID_KEY

TEST_CLIENT_SECRET = 'test_client_secret'
TEST_CLIENT_ID = 'test_client_id'
VALID_CREDENTIALS_FILE = json.dumps({CLIENT_SECRET_KEY: TEST_CLIENT_SECRET, CLIENT_ID_KEY: TEST_CLIENT_ID})
INVALID_CREDENTIALS_FILE = "invalid}"
INVALID_CREDENTIALS_FILE_MISSING_FIELD = json.dumps({CLIENT_SECRET_KEY: TEST_CLIENT_SECRET})


@pytest.mark.usefixtures("mock_config")
@pytest.mark.usefixtures("mock_malformed_config")
class TestSpotifyCredentialLoader(unittest.TestCase):

    def setUp(self):
        pass

    def test_when_config_valid_should_return_correct_credentials(self):
        # mock credential file read
        with mock.patch('builtins.open', mock.mock_open(read_data=VALID_CREDENTIALS_FILE)):
            loader: SpotifyApiCredentialLoader = SpotifyApiCredentialLoader(self.config)
            # assert loader is correctly populated
            assert loader.get_client_secret() == TEST_CLIENT_SECRET
            assert loader.get_client_id() == TEST_CLIENT_ID

    @mock.patch('logging.Logger.error')
    def test_when_config_is_missing_credential_file_address_should_throw_exception_and_log_error(self,
                                                                                                 mock_error_logger):
        with self.assertRaises(configparser.NoOptionError):
            loader: SpotifyApiCredentialLoader = SpotifyApiCredentialLoader(self.malformed_config)
        mock_error_logger.assert_called_once_with(
            '{} not set in config file'.format(CONFIG_SPOTIFY_CREDENTIALS_FILE_NAME_KEY))

    @mock.patch('logging.Logger.error')
    def test_when_config_points_to_incorrect_file_should_throw_exception_and_log_error(self, mock_error_logger):
        with mock.patch('builtins.open', mock.mock_open(read_data=VALID_CREDENTIALS_FILE)) as mock_file_open:
            mock_file_open.side_effect = IOError()
            with self.assertRaises(IOError):
                SpotifyApiCredentialLoader(self.config)
            mock_error_logger.assert_called_once_with('No Spotify credentials file found at {}'.format(
                self.config.get(CONFIG_SECTION, CONFIG_SPOTIFY_CREDENTIALS_FILE_NAME_KEY)))

    @mock.patch('logging.Logger.error')
    def test_when_credential_file_malformed_should_throw_exception_and_log_error(self, mock_error_logger):
        with self.assertRaises(JSONDecodeError):
            with mock.patch('builtins.open', mock.mock_open(read_data=INVALID_CREDENTIALS_FILE)):
                SpotifyApiCredentialLoader(self.config)
        mock_error_logger.assert_called_once_with('Credential file not in json format')

    @mock.patch('logging.Logger.error')
    def test_when_credential_file_missing_fields_should_throw_exception_and_log_error(self, mock_error_logger):
        with self.assertRaises(KeyError):
            with mock.patch('builtins.open', mock.mock_open(read_data=INVALID_CREDENTIALS_FILE_MISSING_FIELD)):
                SpotifyApiCredentialLoader(self.config)
        mock_error_logger.assert_called_once_with("Spotify credentials file is missing some credentials.")
