from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import verify_token
from app.core.database import get_db

from app.services.transaction_service import (
    TransactionService
)

router = APIRouter()


@router.delete("/transaction")
async def delete_transaction(
    order_id: str | None = Query(None),
    bill_number: str | None = Query(None),
    _: bool = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    return await TransactionService.delete_transaction(
        db,
        order_id,
        bill_number
    )