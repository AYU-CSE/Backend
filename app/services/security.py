from datetime import timedelta, datetime

import jwt
import psycopg
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from ..models import Account
from ..repositories import AccountRepository
from ..setting import settings

PRIVATE_KEY = settings.jwt_secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class SecurityService:
    def __init__(self, connection: psycopg.AsyncConnection):
        self.connection = connection
        self.account_repository = AccountRepository(connection)

    def create_access_token(
        self, account: Account, expires_delta: timedelta = None
    ) -> str:
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {"exp": expire, "sub": account.id}

        encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme)
    ) -> Account | None:
        try:
            payload = jwt.decode(token, PRIVATE_KEY, algorithms=[ALGORITHM])
            account_id = payload.get("sub")

            if account_id is None:
                return None
        except InvalidTokenError:
            return None

        account = await self.account_repository.get_account(account_id)

        if account is None:
            return None

        return account
