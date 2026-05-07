from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional
from datetime import date, datetime
from core.models.user import UserStatus
from contracts.document import DocumentReturn

string_255_optional = Field(default=None, max_length=255, min_length=2)
string_255_required = Field(max_length=255, min_length=2)
string_528_optional = Field(default=None, max_length=528, min_length=2)
string_50_optional = Field(default=None, max_length=50, min_length=2)
string_50_required = Field(max_length=50, min_length=2)
string_15_optional = Field(default=None, max_length=15, min_length=2)
string_15_required = Field(max_length=15, min_length=2)
user_status_values = UserStatus.ALL
user_status_error = f"Invalid status. Status must be one of: {', '.join(user_status_values)}"


def validate_user_status(v: Optional[str]):
    if v is None:
        return v
    if v not in user_status_values:
        raise ValueError(user_status_error)
    return v


class UserInputBase(BaseModel):
    name: str = string_255_required
    email: EmailStr
    phone: str = string_15_required
    work_in: str = string_50_required
    how_found_it: Optional[str] = string_255_optional
    desired_transport: Optional[str] = string_255_optional
    birth_date: Optional[date] = None
    invoice: Optional[str] = string_255_optional
    status: Optional[str] = Field(default=UserStatus.PENDING, max_length=20)
    telegram: Optional[str] = string_255_optional
    whatsapp: Optional[str] = string_15_optional
    city: Optional[str] = string_255_optional
    address: Optional[str] = string_528_optional
    citizenship: Optional[str] = Field(default=None, max_length=100, min_length=2)
    consent: bool = False

    @field_validator("status")
    def validate_status(cls, v):
        return validate_user_status(v)

    class Config:
        from_attributes = True


class UserCreate(UserInputBase):
    """Schema for creating a new user"""

    pass

    class Config:
        from_attributes = True


class UserUpdate(UserInputBase):
    name: Optional[str] = string_255_optional
    email: Optional[EmailStr] = None
    phone: Optional[str] = string_15_optional
    work_in: Optional[str] = string_50_optional
    how_found_it: Optional[str] = string_255_optional
    desired_transport: Optional[str] = string_255_optional
    birth_date: Optional[date] = None
    invoice: Optional[str] = string_255_optional
    status: Optional[str] = Field(default=None, max_length=20)
    telegram: Optional[str] = string_255_optional
    whatsapp: Optional[str] = string_15_optional
    city: Optional[str] = string_255_optional
    address: Optional[str] = string_528_optional
    citizenship: Optional[str] = Field(default=None, max_length=100, min_length=2)
    consent: Optional[bool] = None

    @field_validator("status")
    def validate_status(cls, v):
        return validate_user_status(v)

    class Config:
        from_attributes = True


class UserReturn(BaseModel):
    id: int
    created_at: datetime
    name: str
    email: str
    phone: str
    work_in: str
    how_found_it: Optional[str] = None
    desired_transport: Optional[str] = None
    birth_date: Optional[date] = None
    invoice: Optional[str] = None
    status: Optional[str] = UserStatus.PENDING
    telegram: Optional[str] = None
    whatsapp: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    citizenship: Optional[str] = None
    consent: bool = False
    documents: list[DocumentReturn]

    @field_validator("status")
    def validate_status(cls, v):
        return validate_user_status(v)

    class Config:
        from_attributes = True


class UserImportCreate(BaseModel):
    created_at: Optional[datetime] = None
    name: str
    email: str
    phone: str
    how_found_it: Optional[str] = None
    desired_transport: Optional[str] = None
    birth_date: Optional[date] = None
    telegram: Optional[str] = None
    whatsapp: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    work_in: str
    citizenship: Optional[str] = None
    invoice: Optional[str] = None
    status: str = UserStatus.PENDING
    consent: bool = False

    @field_validator("status")
    def validate_status(cls, v):
        return validate_user_status(v)

    class Config:
        from_attributes = True


class UserImportError(BaseModel):
    row: int
    email: Optional[str] = None
    detail: str


class UserImportReport(BaseModel):
    received: int
    imported: int
    skipped: int
    errors: list[UserImportError]
