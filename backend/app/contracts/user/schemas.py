from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from core.models.user import UserStatus

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    work_in: str
    passport_file: Optional[int] = None
    invoice: Optional[str] = None
    status: Optional[str] = UserStatus.PENDING
    telegram: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    stay_type: Optional[str] = None
    insurance_file: Optional[int] = None
    visa_file: Optional[int] = None

    @field_validator("status")
    def validate_status(cls, v):
        if v not in [UserStatus.PENDING, UserStatus.ACTIVE, UserStatus.INACTIVE]:
            raise ValueError(
                f"Invalid status. Status must be one of: {UserStatus.PENDING, UserStatus.ACTIVE, UserStatus.INACTIVE}"
                )
        return v

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    """Schema for creating a new user"""
    pass

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    work_in: Optional[str] = None
    passport_file: Optional[int] = None
    invoice: Optional[str] = None
    status: Optional[str] = UserStatus.PENDING
    telegram: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    stay_type: Optional[str] = None
    insurance_file: Optional[int] = None
    visa_file: Optional[int] = None

    @field_validator("status")
    def validate_status(cls, v):
        if v not in [UserStatus.PENDING, UserStatus.ACTIVE, UserStatus.INACTIVE]:
            raise ValueError(
                f"Invalid status. Status must be one of: {UserStatus.PENDING, UserStatus.ACTIVE, UserStatus.INACTIVE}"
                )
        return v
    class Config:
        from_attributes = True


class UserReturn(UserBase):
    id: int

    class Config:
        from_attributes = True
