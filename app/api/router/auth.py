from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
import uuid
from datetime import datetime, timezone

from app import schemas, services, crud
from app.api import deps

router = APIRouter()


@router.post("/login", response_model=schemas.LoginResponse)
def login_for_session(
    response: Response,  # 쿠키 설정을 위해 Response 객체 필요
    login_request: schemas.LoginRequest,  # JSON body로 받을 경우
    db: Session = Depends(deps.get_db),
):
    """
    사용자 이름과 비밀번호로 로그인하여 세션 ID를 발급받습니다.
    세션 ID는 HttpOnly 쿠키로 설정됩니다.
    """
    user = services.auth.authenticate_user(
        db, username=login_request.username, password=login_request.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 사용자 인증 성공 시 세션 생성
    session = services.auth.create_user_session(db=db, user=user)

    # 쿠키 만료 시간을 UTC로 변환합니다.
    expires_value_for_cookie = session.expires_at
    if isinstance(session.expires_at, datetime):
        dt_obj = session.expires_at
        # datetime 객체가 naive이거나 UTC가 아닌 경우 변환합니다.
        if dt_obj.tzinfo is None or dt_obj.tzinfo.utcoffset(
            dt_obj
        ) != timezone.utc.utcoffset(None):
            if dt_obj.tzinfo is None:
                expires_value_for_cookie = dt_obj.replace(tzinfo=timezone.utc)
            else:
                expires_value_for_cookie = dt_obj.astimezone(timezone.utc)

    # 세션 ID를 HttpOnly 쿠키로 설정 (보안 강화)
    response.set_cookie(
        key=deps.SESSION_COOKIE_NAME,
        value=str(session.id),
        httponly=True,
        # secure=True, # HTTPS 환경에서만 쿠키 전송 (배포 시 True 설정 권장)
        # samesite="lax", # 또는 "strict"
        expires=expires_value_for_cookie,  # 쿠키 만료 시간 설정 (UTC로 변환된 값 사용)
    )

    return schemas.LoginResponse(session_id=session.id)


@router.post("/logout")
async def logout(
    response: Response,
    request: Request,  # 현재 세션 쿠키를 읽기 위해 필요
    db: Session = Depends(deps.get_db),
):
    """
    현재 세션을 삭제하여 로그아웃합니다.
    세션 쿠키를 삭제합니다.
    """
    session_id_str: str | None = request.cookies.get(deps.SESSION_COOKIE_NAME)
    if session_id_str:
        try:
            session_id = uuid.UUID(session_id_str)
            crud.session.delete_session(db, session_id=session_id)
        except ValueError:
            pass  # 잘못된 형식의 쿠키는 무시
        except Exception as e:
            print(f"Error deleting session during logout: {e}")  # 로깅
            # 오류가 발생해도 쿠키는 삭제 시도

    # 클라이언트 측 쿠키 삭제
    response.delete_cookie(key=deps.SESSION_COOKIE_NAME, httponly=True)

    return {"message": "Successfully logged out"}
