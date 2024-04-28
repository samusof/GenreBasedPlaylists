from unittest.mock import patch, Mock

from instance_providers.client_provider import SpotifyClientProvider
from unittest import TestCase


class BaseMock(TestCase):
    def setUp(self):
        self.patchers = []
        self.mock_spotify_client = Mock()
        self.mock_spotify_creds_loader = Mock()
        self.mock_config = Mock()
        self.patchers.append(patch('instance_providers.client_provider.config', self.mock_config))
        self.patchers.append(
            patch('instance_providers.client_provider.SpotifyApiCredentialLoader', self.mock_spotify_creds_loader))
        self.patchers.append(patch('instance_providers.client_provider.SpotifyClient', self.mock_spotify_client))
        [patcher.start() for patcher in self.patchers]

    def tearDown(self):
        [patcher.stop() for patcher in self.patchers]


class TestSpotifyClientProvider(BaseMock):

    def test_given_not_initialised_client_before_should_initialise_one(self):
        mock_spotify_client_instance = self.mock_spotify_client.return_value
        mock_spotify_creds_loader_instance = self.mock_spotify_creds_loader.return_value
        client = SpotifyClientProvider().get_client()
        self.mock_spotify_client.assert_called_once_with(mock_spotify_creds_loader_instance)
        self.mock_spotify_creds_loader.assert_called_once_with(self.mock_config)
        assert client is mock_spotify_client_instance

    def test_given_already_initialised_client_should_return_same_one(self):
        client_provider = SpotifyClientProvider()
        client1 = client_provider.get_client()
        client2 = client_provider.get_client()
        assert client1 is client2

    def test_given_reinitialised_client_provider_should_return_same_client(self):
        client_provider1 = SpotifyClientProvider()
        client_provider2 = SpotifyClientProvider()
        assert client_provider1 == client_provider2
