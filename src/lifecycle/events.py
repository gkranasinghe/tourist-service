import logging
from infrastructure.config.container import shutdown_repository
from infrastructure.config.settings import get_logging_config

# Apply logging configuration once, ideally during application setup
logging.config.dictConfig(get_logging_config())
logger = logging.getLogger("tourist-service")

async def startup():
    logger.info("Starting up the application")
    # Add startup logic here if necessary

async def shutdown():
    logger.info("Shutting down the application")
    shutdown_repository()
    logger.info("Repository and connections closed")
