from pydantic import BaseModel
from datetime import datetime


class Session(BaseModel):
    id: str
    account_id: int
    expires_at: datetime
