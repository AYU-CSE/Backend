from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, base
from app.api.router import account, auth

base.metadata.create_all(bind=engine)

app = FastAPI(title="AYU-CSE API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메소드 (GET, POST 등)
    allow_headers=["*"],  # 허용할 HTTP 헤더
)


@app.get("/")
async def read_root():
    """
    API 서버가 정상적으로 실행 중인지 확인하는 기본 엔드포인트입니다.
    """
    return {"message": "Welcome to AYU-CSE API"}


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(account.router, prefix="/accounts", tags=["accounts"])
