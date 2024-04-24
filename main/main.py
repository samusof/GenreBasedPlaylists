from spotify_api.spotify_api import SpotifyApi, SpotifyApiCredentialLoader
from config import config


def main(api: SpotifyApi):
    api.get_liked_songs()


if __name__ == "__main__":
    spotify_credential_loader = SpotifyApiCredentialLoader(config)
    spotify_api = SpotifyApi(spotify_credential_loader)
    main(spotify_api)
