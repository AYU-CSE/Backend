from typing import Generator, Optional
import uuid
from datetime import datetime, timezone  # timezone을 import 합니다.

from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app import crud, models
from app.database import session_local


# --- DB 세션 의존성 ---
def get_db() -> Generator[Session, None, None]:
    db = session_local()
    try:
        yield db
    finally:
        db.close()


SESSION_COOKIE_NAME = "ayu_cse_session_id"


async def get_current_user(
    request: Request, db: Session = Depends(get_db)
) -> models.Account:
    """
    요청 데이터의 쿠키에서 세션 ID를 읽어 유효성을 검증하고,
    유효한 경우 해당 사용자 객체를 반환합니다.
    """
    session_id_str: Optional[str] = request.cookies.get(SESSION_COOKIE_NAME)
    if not session_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated: No session cookie",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        session_id = uuid.UUID(session_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated: Invalid session ID format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    session = crud.session.get_session(db, session_id=session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated: Invalid session",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 세션 만료 확인
    if session.expires_at and session.expires_at < datetime.now(timezone.utc):
        crud.session.delete_session(db, session_id=session_id)  # 만료된 세션 삭제
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated: Session expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = crud.account.get_account(db, account_id=session.account_id)
    if not user:
        # 세션은 유효하나 해당 유저가 DB에 없는 경우 (비정상 상태)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated: User not found for session",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_active_user(
    current_user: models.Account = Depends(get_current_user),
) -> models.Account:
    return current_user
