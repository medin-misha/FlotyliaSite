from email.policy import default
from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional
from core.models.user import UserStatus
from contracts.document import DocumentReturn

string_field = Field(default=None, max_length=255, min_length=2)


class UserBase(BaseModel):
    name: str = Field(max_length=255, min_length=2)
    email: EmailStr
    phone: str = string_field
    work_in: str = string_field
    invoice: Optional[str] = string_field
    status: Optional[str] = UserStatus.PENDING
    telegram: Optional[str] = string_field
    whatsapp: Optional[str] = string_field
    city: Optional[str] = string_field
    address: Optional[str] = string_field
    stay_type: Optional[str] = string_field

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


class UserUpdate(UserBase):
    name: Optional[str] = string_field
    email: Optional[EmailStr] = None
    phone: Optional[str] = string_field
    work_in: Optional[str] = string_field
    passport_file: Optional[int] = None
    invoice: Optional[str] = string_field
    status: Optional[str] = UserStatus.PENDING
    telegram: Optional[str] = string_field
    whatsapp: Optional[str] = string_field
    city: Optional[str] = string_field
    address: Optional[str] = string_field
    stay_type: Optional[str] = string_field

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
    documents: list[DocumentReturn]

    class Config:
        from_attributes = True
