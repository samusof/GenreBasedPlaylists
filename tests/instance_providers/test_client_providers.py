from unittest.mock import patch, Mock
from instance_providers.client_providers import SpotifyClientProvider, SpotifyApiCredentialLoaderProvider, \
    SpotipyClientProvider
from unittest import TestCase


class BaseMock(TestCase):
    def setUp(self):
        self.patchers = []
        # imported SpotifyApiCredentialLoader class mocked
        self.mock_spotify_creds_loader_class = Mock()
        self.patchers.append(patch('instance_providers.client_providers.SpotifyApiCredentialLoader',
                                   self.mock_spotify_creds_loader_class))
        # imported config mocked
        self.mock_config = Mock()
        self.patchers.append(patch('instance_providers.client_providers.config', self.mock_config))

        # imported Spotify class mocked
        self.mock_spotify_class = Mock()
        self.patchers.append(patch('instance_providers.client_providers.Spotify', self.mock_spotify_class))

        # imported SpotifyOAuth class mocked
        self.mock_spotify_oauth_class = Mock()
        self.patchers.append(patch('instance_providers.client_providers.SpotifyOAuth', self.mock_spotify_oauth_class))
        [patcher.start() for patcher in self.patchers]

        # imported SpotifyClient class mocked
        self.mock_spotify_client_class = Mock()
        self.patchers.append(patch('instance_providers.client_providers.SpotifyClient', self.mock_spotify_client_class))

        [patcher.start() for patcher in self.patchers]

    def tearDown(self):
        [patcher.stop() for patcher in self.patchers]


class TestInstanceProviders(BaseMock):

    def test_when_spotify_cred_loader_provider_created_and_call_get_instance_creates_and_returns_same_instance(self):
        provider = SpotifyApiCredentialLoaderProvider()
        instance1 = provider.get_instance()
        instance2 = provider.get_instance()

        assert instance1 is instance2

    def test_when_spotify_cred_loader_provider_created_twice_returns_same_instance(self):
        provider1 = SpotifyApiCredentialLoaderProvider()
        provider2 = SpotifyApiCredentialLoaderProvider()
        assert provider1 is provider2

    def test_when_spotipy_client_provider_created_and_call_get_instance_creates_and_returns_same_instance(self):
        client_provider = SpotipyClientProvider()
        instance1 = client_provider.get_instance()
        instance2 = client_provider.get_instance()

        assert instance1 is instance2

    def test_when_spotipy_client_provider_created_twice_returns_same_instance(self):
        provider1 = SpotipyClientProvider()
        provider2 = SpotipyClientProvider()
        assert provider1 is provider2

    def test_when_spotify_client_provider_created_and_call_get_instance_creates_and_returns_same_instance(self):
        provider = SpotifyClientProvider()
        instance1 = provider.get_instance()
        instance2 = provider.get_instance()

        assert instance1 is instance2

    def test_when_spotify_client_provider_created_twice_returns_same_instance(self):
        provider1 = SpotifyClientProvider()
        provider2 = SpotifyClientProvider()
        assert provider1 is provider2
