import logging
import logging.config
from fastapi import FastAPI
from infrastructure.controllers.tourist_controller import router as tourist_router
from infrastructure.config.container import shutdown_repository
import os


# Set log level from environment variable (default to 'INFO')
log_level = os.getenv("LOG_LEVEL", "INFO").upper()

# Define logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(asctime)s - %(levelprefix)s - %(message)s",
            "use_colors": True,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",  # Use Uvicorn's access formatter
            "fmt": "%(asctime)s - %(levelprefix)s - %(client_addr)s - \"%(request_line)s\" %(status_code)s",
            "use_colors": True,
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": log_level, "propagate": False},
        "uvicorn.access": {"handlers": ["access"], "level": log_level, "propagate": False},
        "tourist-service": {"handlers": ["default"], "level": log_level, "propagate": False},
    },
}

# Apply logging configuration
logging.config.dictConfig(LOGGING_CONFIG)

# Initialize logger
logger = logging.getLogger("tourist-service")

# Initialize FastAPI application
app = FastAPI()

# Include routes
app.include_router(tourist_router, prefix="/tourists", tags=["tourists"])

async def startup():
    logger.info("Starting up the application")
    # Your startup logic here

async def shutdown():
    logger.info("Start shutting down the application")
    shutdown_repository()
    logger.info("Complete shut down repository")

app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)
