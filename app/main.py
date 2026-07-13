from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.api.routes import router
from app.config import settings
from app.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("=" * 60)
    print(settings.app_name)
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

# Register API Routes
app.include_router(router)


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