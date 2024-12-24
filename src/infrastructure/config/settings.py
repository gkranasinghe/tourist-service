import os
import logging.config
from .config import AppConfig

# Initialize configuration from environment variables
config = AppConfig()

def get_logging_config():
    """Generates a logging configuration dictionary."""
    # Use a specific environment variable for log level or default to 'INFO'
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(asctime)s - %(levelprefix)s - %(message)s",
                "use_colors": True,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
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

    return logging_config


