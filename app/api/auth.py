from typing import Annotated

import psycopg
from fastapi import APIRouter, Depends, HTTPException, Response, status

from ..database import get_connection
from ..models import Session
from ..services import AuthService

auth_router = APIRouter(prefix="/", tags=["auth"])

DatabaseDep = Annotated[psycopg.AsyncConnection, Depends(get_connection)]


@auth_router.post("/token", response_model=Session)
async def get_token(username: str, password: str, database: DatabaseDep):
    auth_service = AuthService(database)

    new_session = await auth_service.activate_session(username, password)

    if new_session is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        return new_session


@auth_router.delete("/token")
async def delete_token(session_id: str, database: DatabaseDep):
    auth_service = AuthService(database)
    result = await auth_service.delete_session(session_id)

    if result is True:
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
