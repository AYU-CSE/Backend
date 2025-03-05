from typing import Annotated

import psycopg
from fastapi import APIRouter, Depends, HTTPException, Response, status

from ..database import get_connection
from ..models import Account
from ..services import AccountService
from .auth import get_current_session

account_router = APIRouter(prefix="/account", tags=["account"])

DatabaseDep = Annotated[psycopg.AsyncConnection, Depends(get_connection)]


@account_router.get("/{account_id}")
async def get_accounts(
    database: DatabaseDep,
    account_id: int,
    session_valid: bool = Depends(get_current_session),
):
    if not session_valid:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    account_service = AccountService(database)
    return await account_service.get_account_by_id(account_id)


@account_router.post("/")
async def create_account(database: DatabaseDep, account: Account):
    account_service = AccountService(database)
    return await account_service.create_account(account)


@account_router.put("/{account_id}")
async def update_account(
    database: DatabaseDep,
    account_id: int,
    account: Account,
    session_valid: bool = Depends(get_current_session),
):
    if not session_valid:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    account_service = AccountService(database)

    if account_id != account.id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Account ID mismatch")

    result = await account_service.update_account(account)

    if result is True:
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@account_router.delete("/{account_id}")
async def delete_account(
    database: DatabaseDep,
    account_id: int,
    session_valid: bool = Depends(get_current_session),
):
    if not session_valid:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    account_service = AccountService(database)

    result = await account_service.delete_account(account_id)

    if result is True:
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
