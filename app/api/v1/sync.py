from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import verify_token
from app.core.database import get_db
from app.schemas.sync_schema import SyncRequest
from app.services.sync_service import SyncService

router = APIRouter()


@router.post("/sync")
async def sync_transaction(
    request: SyncRequest,
    _: bool = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    return await SyncService.sync_transaction(
        db,
        request
    )