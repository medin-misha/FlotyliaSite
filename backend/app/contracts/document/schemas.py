from pydantic import BaseModel, PositiveInt
from typing import Optional

class DocumentBase(BaseModel):
    description: str
    file_id: PositiveInt
    user_id: PositiveInt

    class Config:
        from_attributes = True

class DocumentReturn(DocumentBase):
    id: PositiveInt

    class Config:
        from_attributes = True

class DocumentCreate(DocumentBase): 
    pass

class DocumentUpdate(BaseModel):
    description: Optional[str] = None
    file_id: Optional[PositiveInt] = None
    user_id: Optional[PositiveInt] = None

    class Config:
        from_attributes = True