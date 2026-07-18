"""Durable LangGraph checkpoint factory for SQLite and PostgreSQL."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from app.config import settings

logger = logging.getLogger(__name__)


class CheckpointerFactory:
    """Create one application-lifetime persistent LangGraph checkpointer."""

    _checkpointer: Any | None = None
    _resource: Any | None = None

    @classmethod
    def get(cls) -> Any:
        if cls._checkpointer is not None:
            return cls._checkpointer
        cls._checkpointer = cls._create_postgres() if settings.effective_checkpoint_backend == "postgres" else cls._create_sqlite()
        return cls._checkpointer

    @classmethod
    def close(cls) -> None:
        for resource in (cls._resource, cls._checkpointer):
            close = getattr(resource, "close", None)
            if callable(close):
                close()
        cls._resource = None
        cls._checkpointer = None

    @classmethod
    def _create_sqlite(cls) -> Any:
        try:
            from langgraph.checkpoint.sqlite import SqliteSaver
        except ImportError as exc:
            raise RuntimeError("Install langgraph-checkpoint-sqlite to enable durable checkpoints.") from exc
        path = Path(settings.sqlite_checkpoint_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        saver = SqliteSaver.from_conn_string(str(path))
        setup = getattr(saver, "setup", None)
        if callable(setup):
            setup()
        logger.info("LangGraph checkpoints use SQLite at %s", path)
        return saver

    @classmethod
    def _create_postgres(cls) -> Any:
        try:
            from langgraph.checkpoint.postgres import PostgresSaver
            from psycopg.rows import dict_row
            from psycopg_pool import ConnectionPool
        except ImportError as exc:
            raise RuntimeError("Install PostgreSQL LangGraph checkpoint dependencies.") from exc
        pool = ConnectionPool(
            conninfo=_to_psycopg_url(settings.checkpoint_database_url or settings.database_url),
            min_size=1,
            max_size=4,
            kwargs={"autocommit": True, "prepare_threshold": 0, "row_factory": dict_row},
        )
        saver = PostgresSaver(pool)
        saver.setup()
        cls._resource = pool
        logger.info("LangGraph checkpoints use the configured PostgreSQL database")
        return saver


def _to_psycopg_url(database_url: str) -> str:
    if database_url.startswith("postgresql+"):
        return "postgresql://" + database_url.split("://", 1)[1]
    return database_url
