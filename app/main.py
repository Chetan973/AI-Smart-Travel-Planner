from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.api.booking_routes import router as booking_router
from app.api.chat_routes import router as chat_router
from app.api.payment_routes import router as payment_router
from app.api.routes import router as user_router
from app.api.view_routes import router as view_router
from app.config import settings
from app.database import engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    print("=" * 60)
    print(settings.app_name)
    print("=" * 60)
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("PostgreSQL connected successfully")
    except Exception as exc:
        print("Database connection failed")
        print(exc)
    print("FastAPI started successfully")
    yield
    print("Application shutdown")


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)
app.include_router(user_router)
app.include_router(booking_router)
app.include_router(payment_router)
app.include_router(view_router)
app.include_router(chat_router)


@app.get("/")
def home():
    return {"application": settings.app_name, "version": settings.app_version, "status": "Running", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "UP", "database": "Connected", "application": settings.app_name, "version": settings.app_version}
