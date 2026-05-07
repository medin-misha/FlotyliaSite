from .base import Base
from datetime import date, datetime
from sqlalchemy import String, ForeignKey, Date, DateTime, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

class UserStatus:
    PENDING = "pending"
    ACTIVE = "active"
    INACTIVE = "inoperative"


class User(Base):
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False, index=True)
    how_found_it: Mapped[str] = mapped_column(String(255), nullable=True)
    desired_transport: Mapped[str] = mapped_column(String(255), nullable=True)
    birth_date: Mapped[date] = mapped_column(Date, nullable=True)
    
    telegram: Mapped[str] = mapped_column(String(255), nullable=True)
    whatsapp: Mapped[str] = mapped_column(String(15), nullable=True)
    city: Mapped[str] = mapped_column(String(255), nullable=True)
    address: Mapped[str] = mapped_column(String(528), nullable=True)
    work_in: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    citizenship: Mapped[str] = mapped_column(String(100), nullable=True)
    
    invoice: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=UserStatus.PENDING)
    consent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")

    documents: Mapped[list["Document"]] = relationship("Document", lazy="selectin")