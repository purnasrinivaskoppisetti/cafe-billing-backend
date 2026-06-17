from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from app.core.auth import verify_token
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.services.report_service import (
    ReportService
)

router = APIRouter()


@router.get("/summary")
async def get_summary(
    period: str = Query("day"),
    payment_method: str | None = None,
    device_id: str | None = None,
    _: bool = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    return await ReportService.get_summary(
        db,
        period,
        payment_method,
        device_id
    )