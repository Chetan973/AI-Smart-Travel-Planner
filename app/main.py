from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.config import settings
from app.database import engine

from app.api.routes import router

app.include_router(router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and Shutdown Events
    """

    print("=" * 60)
    print(f"{settings.app_name}")
    print("=" * 60)

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("✅ PostgreSQL Connected Successfully")

    except Exception as ex:
        print("❌ Database Connection Failed")
        print(ex)

    print("🚀 FastAPI Started Successfully")

    yield

    print("👋 Application Shutdown")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan
)




@app.get("/")
def home():
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "Running"
    }


@app.get("/health")
def health():
    return {
        "status": "UP",
        "database": "Connected"
    }