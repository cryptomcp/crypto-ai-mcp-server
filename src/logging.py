"""Logging configuration for the MCP Crypto Bot."""

import sys
from loguru import logger


def get_logger(name: str):
    """Get a logger instance for the given module name."""
    return logger.bind(name=name)
