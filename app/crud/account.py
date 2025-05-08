import warnings
from typing import Union, Dict, Any

from sqlalchemy.orm import Session
from sqlalchemy import select

from app import models, schemas


def get_account(db: Session, account_id: int) -> models.Account | None:
    """ID로 계정 정보를 조회합니다."""
    statement = select(models.Account).where(models.Account.id == account_id)
    return db.execute(statement).scalar_one_or_none()


def get_account_by_email(db: Session, email: str) -> models.Account | None:
    """이메일로 계정 정보를 조회합니다."""
    statement = select(models.Account).where(models.Account.email == email)
    return db.execute(statement).scalar_one_or_none()


def get_account_by_username(db: Session, username: str) -> models.Account | None:
    """사용자 이름으로 계정 정보를 조회합니다."""
    statement = select(models.Account).where(models.Account.username == username)
    return db.execute(statement).scalar_one_or_none()


def get_account_by_student_number(
    db: Session, student_number: str
) -> models.Account | None:
    """학번으로 계정 정보를 조회합니다."""
    statement = select(models.Account).where(
        models.Account.student_number == student_number
    )
    return db.execute(statement).scalar_one_or_none()


def get_accounts(db: Session, skip: int = 0, limit: int = 100) -> list[models.Account]:
    """계정 목록을 조회합니다. (Paging 적용)"""
    statement = select(models.Account).offset(skip).limit(limit)
    return list(db.execute(statement).scalars().all())


def create_account(db: Session, *, account_in: schemas.AccountCreate) -> models.Account:
    """
    새로운 계정을 생성합니다.
    주의: account_in 스키마에는 반드시 '해싱된 비밀번호'가 포함되어야 합니다.
         비밀번호 해싱은 서비스 계층에서 처리 후 이 함수를 호출해야 합니다.
    """
    create_data = account_in.model_dump()
    db_account = models.Account(**create_data)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def update_account(
    db: Session,
    *,
    db_account: models.Account,
    account_in: Union[schemas.AccountUpdate, Dict[str, Any]],  # Union은 그대로 유지
) -> models.Account:
    """기존 계정 정보를 갱신합니다."""
    if isinstance(account_in, dict):
        update_data = account_in
    else:
        update_data = account_in.model_dump(exclude_unset=True)

    if "password" in update_data:
        warnings.warn(
            "Raw password detected in update data. Ensure it's hashed before updating.",
            UserWarning,
        )

    for field, value in update_data.items():
        setattr(db_account, field, value)

    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def delete_account(db: Session, *, account_id: int) -> models.Account | None:
    """ID로 계정을 삭제합니다."""
    db_account = get_account(db, account_id)
    if db_account:
        db.delete(db_account)
        db.commit()
        return db_account
    return None
