from pydantic import BaseModel


class Account(BaseModel):
    id: int
    username: str
    password: str
    email: str
