from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class BoardBase(BaseModel):
    title: str
    content: str
    is_active: bool = True


class BoardCreate(BoardBase):
    pass


class BoardUpdate(BoardBase):
    title: Optional[str] = None
    content: Optional[str] = None
    is_active: Optional[bool] = None


class Board(BoardBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
