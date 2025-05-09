from datetime import datetime
from pydantic import BaseModel


class PermissionCreate(BaseModel):
    user_id: int
    target_id: int


class PermissionResponse(BaseModel):
    id: int
    user_id: int
    target_id: int
    created_at: datetime

    class Config:
        from_attributes = True
