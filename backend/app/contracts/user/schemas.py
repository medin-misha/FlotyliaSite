from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    work_in: str
    passport_url: Optional[str] = None

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    """Schema for creating a new user"""
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    work_in: Optional[str] = None
    passport_url: Optional[str] = None

    class Config:
        from_attributes = True


class UserReturn(UserBase):
    id: int

    class Config:
        from_attributes = True
