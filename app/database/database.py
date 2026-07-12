from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# =====================================================
# SQLAlchemy Engine
# =====================================================

engine = create_engine(
    settings.database_url,
    echo=True
)

# =====================================================
# Session Factory
# =====================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# =====================================================
# Base Class
# =====================================================

Base = declarative_base()


# =====================================================
# Dependency
# =====================================================

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()