from .base import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class ResidencePermit(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    front_side: Mapped[int] = mapped_column(ForeignKey("file.id"), nullable=False)
    back_side: Mapped[int] = mapped_column(ForeignKey("file.id"), nullable=False)
    