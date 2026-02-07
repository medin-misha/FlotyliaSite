from .base import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Document(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    file_id: Mapped[int] = mapped_column(ForeignKey("file.id"), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)