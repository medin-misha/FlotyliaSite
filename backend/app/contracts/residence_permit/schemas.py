from pydantic import BaseModel
from typing import Optional


class ResidencePermitBase(BaseModel):
    user_id: int
    front_side: int
    back_side: int

    class Config:
        from_attributes = True


class ResidencePermitCreate(ResidencePermitBase):
    """Schema for creating a new residence permit"""

    pass


class ResidencePermitUpdate(BaseModel):
    """Schema for updating a residence permit"""

    user_id: Optional[int] = None
    front_side: Optional[int] = None
    back_side: Optional[int] = None

    class Config:
        from_attributes = True


class ResidencePermitReturn(ResidencePermitBase):
    """Schema for returning a residence permit"""

    id: int
