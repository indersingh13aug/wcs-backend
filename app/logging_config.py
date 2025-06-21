# app/logging_config.py
import os
import logging
from logging.config import dictConfig

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # Keeps existing loggers like uvicorn
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
        },
        "access": {
            "format": "%(asctime)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "logs/app.log",
            "formatter": "default",
            "mode": "a",  # Append mode
            "encoding": "utf-8"
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"]
    },
    "loggers": {
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False
        },
        "uvicorn.access": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False
        },
        # Optional: Add your app logger
        "app": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False
        }
    }
}


def setup_logging():
    os.makedirs("logs", exist_ok=True)  # Ensure log dir exists
    dictConfig(LOGGING_CONFIG)
