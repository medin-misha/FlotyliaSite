from pydantic import BaseModel
from typing import Optional

class TransportBase(BaseModel):
    type: str
    manufacturer: str
    model: str
    color: Optional[str] = None
    number: Optional[str] = None

    class Config:
        from_attributes = True

class TransportCreate(TransportBase):
    pass

class TransportUpdate(BaseModel):
    type: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None
    number: Optional[str] = None

    class Config:
        from_attributes = True

class TransportReturn(TransportBase):
    id: int

    class Config:
        from_attributes = True
