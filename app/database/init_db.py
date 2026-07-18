"""Database schema initialization used by app startup and manual setup."""

from app.database import Base, engine
from app import models  # noqa: F401 - registers SQLAlchemy metadata


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
