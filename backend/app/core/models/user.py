from .base import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class UserStatus:
    PENDING = "pending"
    ACTIVE = "active"
    INACTIVE = "inactive"


class User(Base):
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(15), nullable=False, index=True)
    
    telegram: Mapped[str] = mapped_column(String(255), nullable=True)
    city: Mapped[str] = mapped_column(String(255), nullable=True)
    address: Mapped[str] = mapped_column(String(528), nullable=True)
    stay_type: Mapped[str] = mapped_column(String(50), nullable=True)
    work_in: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    passport_file: Mapped[int] = mapped_column(ForeignKey("file.id"), nullable=True)
    insurance_file: Mapped[int] = mapped_column(ForeignKey("file.id"), nullable=True)

    invoice: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=UserStatus.PENDING)