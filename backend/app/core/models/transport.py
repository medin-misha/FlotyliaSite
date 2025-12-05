from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Transport(Base):
   type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
   manufacturer: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
   model: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
   color: Mapped[str] = mapped_column(String(20), nullable=True)
   number: Mapped[str] = mapped_column(String(20), nullable=True)
   
   
   