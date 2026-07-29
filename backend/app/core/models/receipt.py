from sqlalchemy import String, DateTime, Date, Numeric, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from decimal import Decimal
from .base import Base

class Receipt(Base):
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    receipt_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    # Только FK: сам объект File нигде не сериализуется, поэтому relationship не нужен
    # (иначе lazy-загрузка делала бы лишний SELECT на каждый запрос).
    file_id: Mapped[int] = mapped_column(ForeignKey("file.id"), nullable=False)
