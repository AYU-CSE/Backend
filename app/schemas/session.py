import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SessionBase(BaseModel):
    account_id: int
    expires_at: datetime | None


class SessionCreate(SessionBase):
    pass


class SessionRead(SessionBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
