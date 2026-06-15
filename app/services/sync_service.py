from app.repositories.transaction_repository import (
    TransactionRepository
)


class SyncService:

    @staticmethod
    async def sync_transaction(
        db,
        payload
    ):

        transaction = await TransactionRepository.create_transaction(
            db,
            payload
        )

        if transaction is None:
            return {
                "success": False,
                "status_code": 409,
                "message": "Transaction already synced"
            }

        return {
            "success": True,
            "status_code": 200,
            "message": "Transaction synced successfully",
            "transaction_id": transaction.id
        }