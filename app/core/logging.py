"""Logging setup shared by the API and background services."""

import logging

from app.config import settings


def configure_logging() -> None:
    """Configure structured, non-duplicating console logging once."""

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
