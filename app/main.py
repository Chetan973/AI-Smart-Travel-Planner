from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from sqlalchemy import text

from app.api.booking_routes import router as booking_router
from app.api.chat_routes import router as chat_router
from app.api.payment_routes import router as payment_router
from app.api.routes import router as user_router
from app.api.view_routes import router as view_router
from app.config import settings
from app.core.logging import configure_logging
from app.database import Base, engine
from app.graph.checkpoints.factory import CheckpointerFactory

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI):
    configure_logging()
    try:
        Base.metadata.create_all(bind=engine)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        application.state.database_ready = True
        logger.info("Database connected and schema initialized")
    except Exception as exc:
        application.state.database_ready = False
        logger.exception("Database initialization failed: %s", exc)
    yield
    CheckpointerFactory.close()


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
    return {
        "status": "UP",
        "database": "connected" if getattr(app.state, "database_ready", False) else "unavailable",
        "checkpointer": settings.effective_checkpoint_backend,
        "live_search_configured": settings.search_enabled,
        "payments_enabled": settings.razorpay_enabled,
        "application": settings.app_name,
        "version": settings.app_version,
    }
