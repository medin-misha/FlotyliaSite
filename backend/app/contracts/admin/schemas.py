from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BaseAdmin(BaseModel):
    username: str

    class Config:
        from_attributes = True


class AdminCreateForm(BaseAdmin):
    password: str

    class Config:
        from_attributes = True


class AdminCreate(BaseAdmin):
    hashed_password: str

    class Config:
        from_attributes = True


class AdminReturn(BaseAdmin):
    id: int
    hashed_password: str
    last_login_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
