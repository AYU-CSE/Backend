from datetime import datetime
from pydantic import BaseModel


class LikeCreate(BaseModel):
    user_id: int
    target_id: int


class LikeResponse(BaseModel):
    id: int
    user_id: int
    target_id: int
    created_at: datetime

    class Config:
        from_attributes = True
