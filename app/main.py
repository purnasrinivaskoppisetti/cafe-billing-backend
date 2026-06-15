from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import engine
from app.core.database import Base

# Import all models so SQLAlchemy knows about them
from app.models.models import *

from app.api.v1.sync import router as sync_router
from app.api.v1.reports import router as report_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Creating database tables if they do not exist...")

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

    print("Database ready.")

    yield

    print("Application shutdown.")


app = FastAPI(
    title="Coffee Billing Sync API",
    lifespan=lifespan
)

app.include_router(
    sync_router,
    prefix="/api/v1",
    tags=["Sync"]
)


app.include_router(
    report_router,
    prefix="/api/v1/reports",
    tags=["Reports"]
)
app.include_router(
    report_router,
    prefix="/api/v1/reports",
    tags=["Reports"]
)