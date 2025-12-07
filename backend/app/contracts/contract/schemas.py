from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class ContractBase(BaseModel):
    contract_url: str
    transport_id: int
    user_id: int
    date_of_signing: Optional[datetime] = None
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True

class ContractCreate(ContractBase):
    pass

class ContractUpdate(BaseModel):
    contract_url: Optional[str] = None
    transport_id: Optional[int] = None
    user_id: Optional[int] = None
    date_of_signing: Optional[datetime] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True

class ContractReturn(ContractBase):
    id: int

    class Config:
        from_attributes = True
