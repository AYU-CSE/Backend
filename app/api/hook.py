from fastapi import APIRouter

from .account import account_router
from .auth import auth_router

api_router = APIRouter()

api_router.include_router(account_router)
api_router.include_router(auth_router)
