from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class ContractBase(BaseModel):
    contract_file: Optional[int] = None
    transport_id: int
    user_id: int
    date_of_signing: Optional[datetime] = None
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True

class ContractCreate(ContractBase):
    pass

    class Config:
        from_attributes = True

class ContractUpdate(BaseModel):
    contract_file: Optional[int] = None
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
