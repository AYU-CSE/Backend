from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class GroupBase(BaseModel):
    name: str
    is_active: bool = True


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    name: Optional[str] = None
    is_active: Optional[bool] = None


class Group(GroupBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
