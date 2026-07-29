from pydantic import BaseModel, Field
from datetime import datetime, date
from decimal import Decimal
from typing import Optional


class ReceiptBase(BaseModel):
    receipt_date: date
    amount: Decimal = Field(gt=0)  # деньги — точный Decimal, а не float
    description: Optional[str] = Field(default=None, max_length=500)
    file_id: int

    class Config:
        from_attributes = True

class ReceiptCreate(ReceiptBase):
    pass

    class Config:
        from_attributes = True

class ReceiptUpdate(BaseModel):
    receipt_date: Optional[date] = None
    amount: Optional[Decimal] = Field(default=None, gt=0)
    description: Optional[str] = Field(default=None, max_length=500)
    file_id: Optional[int] = None

    class Config:
        from_attributes = True

class ReceiptReturn(ReceiptBase):
    id: int
    created_date: datetime

    class Config:
        from_attributes = True

class MonthlyStat(BaseModel):
    year: int
    month: int
    total_amount: Decimal
