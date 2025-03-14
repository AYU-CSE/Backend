from typing import Annotated

from pydantic import AfterValidator, BaseModel, EmailStr, Field

allowed_domains = ["@gs.anyang.ac.kr", "@anyang.ac.kr"]


def email_validator(value: EmailStr) -> EmailStr:
    if value is None:
        return value

    for domain in allowed_domains:
        if value.endswith(domain):
            return value

    raise ValueError(f"email should be ended with: {', '.join(allowed_domains)}")


class Account(BaseModel):
    id: int
    username: str
    nickname: str
    password: str
    email: EmailStr
    student_number: str

    class Config:
        extra = "ignore"


class CreateAccountDTO(BaseModel):
    username: str = Field(..., min_length=10, max_length=50)
    nickname: str = Field(..., min_length=10, max_length=50)
    password: str = Field(..., min_length=12, max_length=100)
    email: Annotated[EmailStr, AfterValidator(email_validator)]
    student_number: str = Field(..., pattern=r"^\d{4}[A-Z]\d{4}$")

    class Config:
        extra = "ignore"


class UpdateAccountDTO(BaseModel):
    username: str | None = Field(None, min_length=10, max_length=50)
    nickname: str | None = Field(None, min_length=10, max_length=50)
    password: str | None = Field(None, min_length=12, max_length=100)
    email: Annotated[EmailStr, AfterValidator(email_validator)] | None
    student_number: str | None = Field(None, pattern=r"^\d{4}[A-Z]\d{4}$")

    class Config:
        extra = "ignore"


class GetAccountDTO(BaseModel):
    id: int
    username: str
    nickname: str
    email: EmailStr
    student_number: str

    class Config:
        extra = "ignore"
