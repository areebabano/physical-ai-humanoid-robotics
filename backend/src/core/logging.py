import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logger(name: str = __name__, level: int = logging.INFO):
    """
    Set up a logger with both console and file handlers
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent adding handlers multiple times
    if logger.handlers:
        return logger

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)

    return logger


# Create a default logger instance
logger = setup_logger()