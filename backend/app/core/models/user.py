from .base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(15), nullable=False, index=True)
    work_in: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    passport_url: Mapped[str] = mapped_column(String(255), nullable=True)