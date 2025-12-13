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


class AdminAuth(BaseAdmin):
    username: str
    password: bytes

    class Config:
        from_attributes = True


class JWToken(BaseModel):
    access_token: str
    token_type: str


class RawJWTPayload(BaseModel):
    sub: str  # Admin.username


class JWTPayload(RawJWTPayload):
    exp: int | float  # время жизни токена
    iat: int | float  # время создания токена
