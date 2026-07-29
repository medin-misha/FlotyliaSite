from sqlalchemy import select, func, extract
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Receipt
from services.error_handlers import DBErrorHandler


async def get_monthly_statistics(session: AsyncSession) -> list[dict]:
    """
    💡 Месячная статистика расходов по чекам.

    Группирует чеки по году и месяцу поля `receipt_date` и суммирует `amount`.

    Returns:
        Список словарей вида {"year": int, "month": int, "total_amount": Decimal},
        отсортированный по году и месяцу.
    """
    try:
        stmt = (
            select(
                extract("year", Receipt.receipt_date).label("year"),
                extract("month", Receipt.receipt_date).label("month"),
                func.sum(Receipt.amount).label("total_amount"),
            )
            .group_by("year", "month")
            .order_by("year", "month")
        )
        rows = (await session.execute(stmt)).all()
        return [
            {
                "year": int(row.year),
                "month": int(row.month),
                "total_amount": row.total_amount,  # Decimal — точная сумма без потери на float
            }
            for row in rows
        ]
    except Exception as err:
        DBErrorHandler.handle(err=err, model=Receipt)
