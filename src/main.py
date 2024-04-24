from api.v1.service import app
from app_logging.logger import logger
import uvicorn
from src.spotify.client import SpotifyApi, SpotifyApiCredentialLoader, SpotifyClient
from config import config


def main():
    logger.info("Running service")
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    spotify_credential_loader = SpotifyApiCredentialLoader(config)
    api = SpotifyClient().get_client()
    api.get_liked_songs()
    main()
