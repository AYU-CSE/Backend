from pydantic import BaseModel


class Account(BaseModel):
    id: int
    username: str
    nickname: str
    password: str
    email: str
    student_number: str
