from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app import crud, models, schemas
from app.core.security import get_password_hash


def create_account(db: Session, *, account_in: schemas.AccountCreate) -> models.Account:
    if crud.account.get_account_by_username(db, username=account_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    if crud.account.get_account_by_email(db, email=str(account_in.email)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    if crud.account.get_account_by_student_number(
        db, student_number=account_in.student_number
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student number already registered",
        )

    hashed_password = get_password_hash(account_in.password)

    create_data = account_in.model_dump(exclude={"password"})  # password 필드 제외
    create_data["password"] = hashed_password  # 해시된 비밀번호 추가

    db_account = crud.account.create_account(
        db=db, account_in=schemas.AccountCreate(**create_data)
    )  # 임시 스키마 변환 또는 CRUD 수정 필요

    return db_account
