"""Logging utilities for the Ge'ez-Script NLP survey pipeline.

Provides centralized logging configuration for console and file output
with consistent formatting across all pipeline components.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str, log_file: Optional[str] = None, level: int = logging.DEBUG
) -> logging.Logger:
    """Configure and return a logger instance.

    Sets up logging with both console and optional file output. Console logging
    is set to INFO level, while file logging is set to DEBUG level for detailed
    troubleshooting.

    Args:
        name: Logger name (typically __name__ from calling module)
        log_file: Optional path to log file for file output
        level: Logging level for the logger (default: DEBUG)

    Returns:
        Configured logging.Logger instance

    Example:
        >>> logger = setup_logger(__name__, log_file="logs/pipeline.log")
        >>> logger.info("Pipeline started")
        >>> logger.debug("Detailed debugging information")
    """
    logger = logging.getLogger(name)

    # Avoid duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # Format with timestamp, logger name, level, and message
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler - INFO level for user-facing messages
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler - DEBUG level for detailed logging
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.debug(f"Logging to file: {log_path.absolute()}")

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance by name.

    Returns an existing logger if already configured, or creates a new one.
    Use this when you want to use a logger without configuring it again.

    Args:
        name: Logger name

    Returns:
        logging.Logger instance
    """
    return logging.getLogger(name)


def disable_logger(name: str) -> None:
    """Disable logging for a specific logger.

    Args:
        name: Logger name to disable
    """
    logging.getLogger(name).disabled = True


def enable_logger(name: str) -> None:
    """Enable logging for a specific logger.

    Args:
        name: Logger name to enable
    """
    logging.getLogger(name).disabled = False


def set_log_level(name: str, level: int) -> None:
    """Set the logging level for a specific logger.

    Args:
        name: Logger name
        level: Logging level (e.g., logging.DEBUG, logging.INFO, logging.WARNING)
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)


def clear_handlers(name: str) -> None:
    """Clear all handlers from a logger.

    Useful when reconfiguring logging for a module.

    Args:
        name: Logger name
    """
    logger = logging.getLogger(name)
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)
