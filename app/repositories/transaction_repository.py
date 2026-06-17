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
    


    @staticmethod
    async def delete_transaction(
        db,
        order_id: str | None = None,
        bill_number: str | None = None
    ):

        if not order_id and not bill_number:
            return {
                "success": False,
                "message": "order_id or bill_number is required"
            }

        query = select(Transaction)

        if order_id:
            query = query.where(
                Transaction.id == order_id
            )

        elif bill_number:
            query = query.where(
                Transaction.bill_number == bill_number
            )

        result = await db.execute(query)

        transaction = result.scalar_one_or_none()

        if not transaction:
            return {
                "success": False,
                "message": "Transaction not found"
            }

        await db.delete(transaction)

        await db.commit()

        return {
            "success": True,
            "message": "Transaction deleted successfully",
            "transaction_id": transaction.id,
            "bill_number": transaction.bill_number
        }