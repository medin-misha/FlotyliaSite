from sqlalchemy import String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .base import Base

class Contract(Base):
    contract_url: Mapped[str] = mapped_column(String(255), nullable=False)
    transport_id: Mapped[int] = mapped_column(ForeignKey("transport.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    date_of_signing: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)