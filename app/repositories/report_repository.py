from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy import func

from app.models.models import (
    Transaction,
    TransactionItem
)


class ReportRepository:

    @staticmethod
    async def get_summary(
        db,
        period: str,
        payment_method: str | None = None
    ):

        now = datetime.utcnow()

        if period == "day":
            # Yesterday
            start_date = now - timedelta(days=1)

        elif period == "week":
            start_date = now - timedelta(days=7)

        elif period == "month":
            start_date = now - timedelta(days=30)

        else:
            start_date = datetime.min

        summary_query = (
            select(
                func.count(
                    func.distinct(Transaction.id)
                ),
                func.coalesce(
                    func.sum(Transaction.grand_total),
                    0
                ),
                func.coalesce(
                    func.sum(Transaction.discount),
                    0
                ),
                func.coalesce(
                    func.sum(TransactionItem.qty),
                    0
                )
            )
            .outerjoin(
                TransactionItem,
                Transaction.id ==
                TransactionItem.transaction_id
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

        summary_result = await db.execute(
            summary_query
        )

        (
            total_transactions,
            total_revenue,
            total_discount,
            total_products_sold
        ) = summary_result.first()

        # Product-wise sales
        product_query = (
            select(
                TransactionItem.name,
                func.sum(
                    TransactionItem.qty
                ).label("qty_sold")
            )
            .join(
                Transaction,
                Transaction.id ==
                TransactionItem.transaction_id
            )
            .where(
                Transaction.created_at >= start_date
            )
            .group_by(
                TransactionItem.name
            )
            .order_by(
                func.sum(
                    TransactionItem.qty
                ).desc()
            )
        )

        if payment_method:
            product_query = product_query.where(
                Transaction.payment_method ==
                payment_method
            )

        product_result = await db.execute(
            product_query
        )

        products = []

        for row in product_result:
            products.append({
                "product_name": row.name,
                "quantity_sold": row.qty_sold
            })

        # Daily revenue breakdown
        sales_query = (
            select(
                func.date(
                    Transaction.created_at
                ).label("date"),
                func.sum(
                    Transaction.grand_total
                ).label("revenue")
            )
            .where(
                Transaction.created_at >= start_date
            )
            .group_by(
                func.date(
                    Transaction.created_at
                )
            )
            .order_by(
                func.date(
                    Transaction.created_at
                )
            )
        )

        if payment_method:
            sales_query = sales_query.where(
                Transaction.payment_method ==
                payment_method
            )

        sales_result = await db.execute(
            sales_query
        )

        daily_sales = []

        for row in sales_result:
            daily_sales.append({
                "date": str(row.date),
                "revenue": float(row.revenue)
            })

        return {
            "total_transactions": total_transactions,
            "total_revenue": float(total_revenue),
            "total_discount": float(total_discount),
            "total_products_sold": total_products_sold,
            "product_sales": products,
            "daily_sales": daily_sales
        }