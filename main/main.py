from spotify_api.spotify_api import SpotifyApi
from config import config

api: SpotifyApi = SpotifyApi(config)
api.get_liked_songs()
