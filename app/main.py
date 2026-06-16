from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base

# Import all models so SQLAlchemy knows about them
from app.models.models import *

from app.api.v1.sync import router as sync_router
from app.api.v1.reports import router as report_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Creating database tables if they do not exist...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Database ready.")

    yield

    print("Application shutdown.")


app = FastAPI(
    title="Coffee Billing Sync API",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8081",
        "https://yourdomain.com",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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