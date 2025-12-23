from sqlalchemy import String, DateTime, ForeignKey, Boolean, func, Integer
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .base import Base

class Contract(Base):
    contract_file: Mapped[int] = mapped_column(ForeignKey("file.id"), nullable=False)
    transport_id: Mapped[int] = mapped_column(ForeignKey("transport.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    date_of_signing: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)