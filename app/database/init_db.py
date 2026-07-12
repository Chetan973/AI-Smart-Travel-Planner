from app.database import Base
from app.database import engine

# Import all models
from app.models import *


def create_tables():

    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully.")


if __name__ == "__main__":
    create_tables()