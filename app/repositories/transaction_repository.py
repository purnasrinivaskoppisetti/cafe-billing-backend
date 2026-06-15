from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import (
    Transaction,
    TransactionItem,
    SyncLog
)


class TransactionRepository:

    @staticmethod
    async def create_transaction(
        db: AsyncSession,
        payload
    ):

        existing = await db.scalar(
            select(Transaction).where(
                Transaction.id == payload.transaction.id
            )
        )

        if existing:
            return None

        transaction = Transaction(
            id=payload.transaction.id,
            bill_number=payload.transaction.bill_number,
            total_items=payload.transaction.total_items,
            sub_total=payload.transaction.sub_total,
            discount=payload.transaction.discount,
            grand_total=payload.transaction.grand_total,
            payment_method=payload.transaction.payment_method,
            created_at=payload.transaction.created_at,
            synced_at=datetime.utcnow(),
            device_id=payload.device_id
        )

        db.add(transaction)

        for item in payload.items:

            db.add(
                TransactionItem(
                    transaction_id=payload.transaction.id,
                    product_id=item.product_id,
                    name=item.name,
                    rate=item.rate,
                    qty=item.qty
                )
            )

        db.add(
            SyncLog(
                transaction_id=payload.transaction.id,
                device_id=payload.device_id,
                synced_at=datetime.utcnow()
            )
        )

        await db.commit()
        await db.refresh(transaction)

        return transaction