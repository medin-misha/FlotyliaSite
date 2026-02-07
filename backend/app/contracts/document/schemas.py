from pydantic import BaseModel, PositiveInt

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