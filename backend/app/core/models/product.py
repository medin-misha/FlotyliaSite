from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Boolean, func, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class IncidentType:
    DAMAGE = "damage"
    THEFT = "theft"
    OTHER = "other"

class IncidentStatus:
    OPEN = "open"
    CLOSED = "closed"
    RESOLVED = "resolved"
    IN_PROGRESS = "in_progress"

class Product(Base):
    name: Mapped[str] = mapped_column(String(120))
    price: Mapped[int] = mapped_column(Integer, default=0)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    description: Mapped[str] = mapped_column(String(500), default="")
    date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    contract_id: Mapped[int] = mapped_column(ForeignKey("contract.id"))
    type: Mapped[str] = mapped_column(String(20), default=IncidentType.OTHER)
    status: Mapped[str] = mapped_column(String(20), default=IncidentStatus.OPEN)