from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class AccountBase(BaseModel):
    username: str
    nickname: str
    email: EmailStr
    student_number: str


class AccountCreate(AccountBase):
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "username": "new_user",
                    "nickname": "Newbie",
                    "email": "new_user@gs.anyang.ac.kr",
                    "student_number": "2025E1234",
                    "password": "password123",
                }
            ]
        }
    )


class AccountUpdate(BaseModel):
    username: Optional[str] = None
    nickname: Optional[str] = None
    email: Optional[EmailStr] = None
    student_number: Optional[str] = None
    password: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"nickname": "Updated Nickname", "password": "newpassword456"}]
        }
    )


class AccountRead(AccountBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
