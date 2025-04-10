from typing import Annotated
from uuid import UUID

import psycopg
from fastapi import APIRouter, Depends, Header, HTTPException, Response, status

from ..database import get_connection
from ..models.account import GetAccountDTO
from ..models.session import Session
from ..services import AuthService

auth_router = APIRouter(tags=["auth"])

DatabaseDep = Annotated[psycopg.AsyncConnection, Depends(get_connection)]


async def get_current_account(
    database: DatabaseDep, session_id: UUID = Header(...)
) -> GetAccountDTO | None:
    auth_service = AuthService(database)
    return await auth_service.get_account_from_session(session_id)


@auth_router.post("/token", response_model=Session)
async def get_token(database: DatabaseDep, username: str, password: str):
    auth_service = AuthService(database)

    new_session = await auth_service.activate_session(username, password)

    if new_session is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        return new_session


@auth_router.delete("/token")
async def delete_token(database: DatabaseDep, session_id: UUID = Header(...)):
    auth_service = AuthService(database)
    result = await auth_service.delete_session(session_id)

    if result is True:
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
