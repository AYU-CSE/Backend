from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Session(BaseModel):
    id: UUID
    account_id: int
    expires_at: datetime
