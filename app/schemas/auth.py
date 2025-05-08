from pydantic import BaseModel
import uuid


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    session_id: uuid.UUID
