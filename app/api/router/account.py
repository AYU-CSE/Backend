from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, services, models
from app.api import deps

router = APIRouter()


@router.post(
    "/", response_model=schemas.AccountRead, status_code=status.HTTP_201_CREATED
)
def create_account(
    *,
    db: Session = Depends(deps.get_db),
    account_in: schemas.AccountCreate,  # API 요청 본문 스키마
):
    """
    새로운 사용자 계정을 생성합니다.
    Username, Email, Student Number는 고유해야 합니다.
    """
    # 서비스 계층 호출
    try:
        account = services.account.create_account(db, account_in=account_in)
    except HTTPException as e:
        # 서비스 계층에서 발생한 HTTPException을 그대로 전달
        raise e
    except Exception as e:
        # 예상치 못한 다른 오류 처리
        print(f"Error creating account: {e}")  # 로깅 권장
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
    return account


@router.get("/me", response_model=schemas.AccountRead)
async def read_account_me(
    current_user: models.Account = Depends(deps.get_current_active_user),  # 로그인 필요
):
    """
    현재 로그인된 사용자 본인의 계정 정보를 가져옵니다.
    """
    return current_user
