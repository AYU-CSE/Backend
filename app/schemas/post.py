from datetime import datetime
from pydantic import BaseModel


class PostCreate(BaseModel):
    board_id: int
    title: str
    content: str

class PostUpdate(BaseModel):
    board_id: int
    title: str | None = None
    content: str | None = None

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
