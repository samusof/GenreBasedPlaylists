from api.v1.service import app
from app_logging.logger import logger
import uvicorn


def main():
    logger.info("Running service")
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
