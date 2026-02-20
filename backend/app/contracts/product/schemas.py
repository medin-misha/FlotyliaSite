from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ProductBase(BaseModel):
    name: str = Field(max_length=120)
    price: int = Field(default=0, ge=0)
    quantity: int = Field(default=0, ge=0)
    description: Optional[str] = Field(default="", max_length=500)
    contract_id: int
    type: str = Field(default="other", max_length=20)
    status: str = Field(default="open", max_length=20)

    class Config:
        from_attributes = True

class ProductCreate(ProductBase):
    pass

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=120)
    price: Optional[int] = Field(default=None, ge=0)
    quantity: Optional[int] = Field(default=None, ge=0)
    description: Optional[str] = Field(default=None, max_length=500)
    contract_id: Optional[int] = None
    type: Optional[str] = Field(default=None, max_length=20)
    status: Optional[str] = Field(default=None, max_length=20)

    class Config:
        from_attributes = True

class ProductReturn(ProductBase):
    id: int

    class Config:
        from_attributes = True
