from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional
from core.models.user import UserStatus
from contracts.document import DocumentReturn

string_255_optional = Field(default=None, max_length=255, min_length=2)
string_255_required = Field(max_length=255, min_length=2)
string_528_optional = Field(default=None, max_length=528, min_length=2)
string_50_optional = Field(default=None, max_length=50, min_length=2)
string_50_required = Field(max_length=50, min_length=2)
string_15_optional = Field(default=None, max_length=15, min_length=2)
string_15_required = Field(max_length=15, min_length=2)


class UserBase(BaseModel):
    name: str = string_255_required
    email: EmailStr
    phone: str = string_15_required
    work_in: str = string_50_required
    how_found_it: Optional[str] = string_255_optional
    invoice: Optional[str] = string_255_optional
    status: Optional[str] = Field(default=UserStatus.PENDING, max_length=20)
    telegram: Optional[str] = string_255_optional
    whatsapp: Optional[str] = string_15_optional
    city: Optional[str] = string_255_optional
    address: Optional[str] = string_528_optional
    stay_type: Optional[str] = string_50_optional

    @field_validator("status")
    def validate_status(cls, v):
        if v is None:
            return v
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
    name: Optional[str] = string_255_optional
    email: Optional[EmailStr] = None
    phone: Optional[str] = string_15_optional
    work_in: Optional[str] = string_50_optional
    how_found_it: Optional[str] = string_255_optional
    invoice: Optional[str] = string_255_optional
    status: Optional[str] = Field(default=None, max_length=20)
    telegram: Optional[str] = string_255_optional
    whatsapp: Optional[str] = string_15_optional
    city: Optional[str] = string_255_optional
    address: Optional[str] = string_528_optional
    stay_type: Optional[str] = string_50_optional

    @field_validator("status")
    def validate_status(cls, v):
        if v is None:
            return v
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
