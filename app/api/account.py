from typing import Annotated

import psycopg
from fastapi import APIRouter, Depends

from ..database import get_connection
from ..services import AccountService
from ..models import Account

ConnectionDep = Annotated[psycopg.Connection, Depends(get_connection)]
account_router = APIRouter(prefix="/account", tags=["account"])


@account_router.get("/{account_id}")
async def get_accounts(account_id: int, connection: ConnectionDep):
    account_service = AccountService(connection)

    return await account_service.get_account(account_id)
