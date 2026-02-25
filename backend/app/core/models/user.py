from .base import Base
from datetime import date
from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

class UserStatus:
    PENDING = "pending"
    ACTIVE = "active"
    INACTIVE = "inoperative"


class User(Base):
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(15), nullable=False, index=True)
    how_found_it: Mapped[str] = mapped_column(String(255), nullable=True)
    desired_transport: Mapped[str] = mapped_column(String(255), nullable=True)
    birth_date: Mapped[date] = mapped_column(Date, nullable=True)
    
    telegram: Mapped[str] = mapped_column(String(255), nullable=True)
    whatsapp: Mapped[str] = mapped_column(String(15), nullable=True)
    city: Mapped[str] = mapped_column(String(255), nullable=True)
    address: Mapped[str] = mapped_column(String(528), nullable=True)
    stay_type: Mapped[str] = mapped_column(String(50), nullable=True)
    work_in: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    invoice: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=UserStatus.PENDING)

    documents: Mapped[list["Document"]] = relationship("Document", lazy="selectin")
