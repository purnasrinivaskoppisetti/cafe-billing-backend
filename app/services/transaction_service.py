from app.repositories.transaction_repository import (
    TransactionRepository
)


class TransactionService:

    @staticmethod
    async def delete_transaction(
        db,
        order_id=None,
        bill_number=None
    ):
        return await TransactionRepository.delete_transaction(
            db,
            order_id,
            bill_number
        )