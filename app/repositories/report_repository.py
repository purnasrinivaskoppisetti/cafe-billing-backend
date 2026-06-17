from datetime import datetime, timedelta

from sqlalchemy import select, func

from app.models.models import (
    Transaction,
    TransactionItem
)


class ReportRepository:

    @staticmethod
    async def get_summary(
        db,
        period: str,
        payment_method: str | None = None,
        device_id: str | None = None
    ):

        now = datetime.utcnow()

        if period == "day":
            start_date = now - timedelta(days=1)

        elif period == "week":
            start_date = now - timedelta(days=7)

        elif period == "month":
            start_date = now - timedelta(days=30)

        else:
            start_date = datetime.min

        # ----------------------------------------
        # Device Summary
        # ----------------------------------------

        summary_query = (
            select(
                Transaction.device_id,
                func.count(
                    Transaction.id
                ).label(
                    "total_transactions"
                ),
                func.coalesce(
                    func.sum(
                        Transaction.grand_total
                    ),
                    0
                ).label(
                    "total_revenue"
                ),
                func.coalesce(
                    func.sum(
                        Transaction.discount
                    ),
                    0
                ).label(
                    "total_discount"
                )
            )
            .where(
                Transaction.created_at >= start_date
            )
        )

        if payment_method:
            summary_query = summary_query.where(
                Transaction.payment_method ==
                payment_method
            )

        if device_id:
            summary_query = summary_query.where(
                Transaction.device_id ==
                device_id
            )

        summary_query = summary_query.group_by(
            Transaction.device_id
        )

        summary_result = await db.execute(
            summary_query
        )

        devices = {}

        for row in summary_result:

            devices[row.device_id] = {
                "device_id": row.device_id,
                "total_transactions": row.total_transactions,
                "total_revenue": float(
                    row.total_revenue or 0
                ),
                "total_discount": float(
                    row.total_discount or 0
                ),
                "total_products_sold": 0,
                "product_sales": [],
                "daily_sales": []
            }

        # ----------------------------------------
        # Product-wise Sales
        # ----------------------------------------

        product_query = (
            select(
                Transaction.device_id,
                TransactionItem.name,
                func.sum(
                    TransactionItem.qty
                ).label(
                    "qty_sold"
                )
            )
            .join(
                Transaction,
                Transaction.id ==
                TransactionItem.transaction_id
            )
            .where(
                Transaction.created_at >= start_date
            )
        )

        if payment_method:
            product_query = product_query.where(
                Transaction.payment_method ==
                payment_method
            )

        if device_id:
            product_query = product_query.where(
                Transaction.device_id ==
                device_id
            )

        product_query = (
            product_query
            .group_by(
                Transaction.device_id,
                TransactionItem.name
            )
            .order_by(
                Transaction.device_id
            )
        )

        product_result = await db.execute(
            product_query
        )

        for row in product_result:

            if row.device_id not in devices:
                continue

            qty = int(
                row.qty_sold or 0
            )

            devices[row.device_id][
                "total_products_sold"
            ] += qty

            devices[row.device_id][
                "product_sales"
            ].append({
                "product_name": row.name,
                "quantity_sold": qty
            })

        # ----------------------------------------
        # Daily Sales
        # ----------------------------------------

        sales_query = (
            select(
                Transaction.device_id,
                func.date(
                    Transaction.created_at
                ).label(
                    "date"
                ),
                func.coalesce(
                    func.sum(
                        Transaction.grand_total
                    ),
                    0
                ).label(
                    "revenue"
                )
            )
            .where(
                Transaction.created_at >= start_date
            )
        )

        if payment_method:
            sales_query = sales_query.where(
                Transaction.payment_method ==
                payment_method
            )

        if device_id:
            sales_query = sales_query.where(
                Transaction.device_id ==
                device_id
            )

        sales_query = (
            sales_query
            .group_by(
                Transaction.device_id,
                func.date(
                    Transaction.created_at
                )
            )
            .order_by(
                Transaction.device_id,
                func.date(
                    Transaction.created_at
                )
            )
        )

        sales_result = await db.execute(
            sales_query
        )

        for row in sales_result:

            if row.device_id not in devices:
                continue

            devices[row.device_id][
                "daily_sales"
            ].append({
                "date": str(
                    row.date
                ),
                "revenue": float(
                    row.revenue or 0
                )
            })

        return {
            "devices": list(
                devices.values()
            )
        }