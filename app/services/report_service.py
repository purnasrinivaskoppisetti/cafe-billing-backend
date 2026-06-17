from app.repositories.report_repository import (
    ReportRepository
)


class ReportService:

    @staticmethod
    async def get_summary(
        db,
        period,
        payment_method=None,
        device_id=None
    ):
        return await ReportRepository.get_summary(
            db,
            period,
            payment_method,
            device_id
        )