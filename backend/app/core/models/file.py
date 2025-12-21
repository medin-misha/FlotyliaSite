from .base import Base  
from sqlalchemy import Column, String, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class File(Base):
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())
    link: Mapped[str] = mapped_column(String(255), nullable=False)