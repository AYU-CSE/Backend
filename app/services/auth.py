from sqlalchemy.orm import Session
from datetime import timedelta
from app import crud, models
from app.core.security import verify_password


def authenticate_user(
    db: Session, *, username: str, password: str
) -> models.Account | None:
    """사용자 인증 (로그인 시 사용)"""
    user = crud.account.get_account_by_username(db, username=username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_user_session(db: Session, *, user: models.Account) -> models.Session:
    """사용자 인증 성공 후 세션 생성"""
    expires_delta = timedelta(hours=1)
    session = crud.session.create_session(
        db=db, account_id=user.id, expires_delta=expires_delta
    )
    return session
