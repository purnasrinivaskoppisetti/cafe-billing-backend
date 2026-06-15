from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.sync_schema import SyncRequest
from app.services.sync_service import SyncService

router = APIRouter()


@router.post("/sync")
async def sync_transaction(
    request: SyncRequest,
    db: AsyncSession = Depends(get_db)
):

    return await SyncService.sync_transaction(
        db,
        request
    )