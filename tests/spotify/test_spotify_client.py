from unittest import TestCase
from unittest.mock import patch, Mock

import pytest

from spotify.client import SpotifyClient


@pytest.mark.usefixtures("mock_spotify_api_creds_loader")
class TestSpotifyClient(TestCase):

    def test_when_initialised_correctly_sets_the_credentials_and_gets_spotipy_api(self):
        pass

    def test_when_credentials_missing_raises_exception(self):

        pass

    def test_when_correctly_initialised_calls_get_liked_songs_spotipy_api_returns_top_liked_tracks(self):
        pass

    def test_when_spotipy_api_fails_returns_empty_list_and_logs_error(self):
        pass

    def test_when_offset_passed_to_get_liked_songs_calls_spotipy_with_offset(self):
        pass
