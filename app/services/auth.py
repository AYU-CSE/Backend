from datetime import datetime, timezone, timedelta
from uuid import UUID, uuid4

import psycopg

from ..models import Account, Session
from ..repositories import AccountRepository, SessionRepository
from ..setting import settings
from ..utils.password import verify_password


class AuthService:
    def __init__(self, connection: psycopg.AsyncConnection):
        self.connection = connection
        self.account_repository = AccountRepository(connection)
        self.session_repository = SessionRepository(connection)

    async def activate_session(self, username: str, password: str) -> Session | None:
        account = await self.account_repository.read_by_username(username)

        if account is None:
            return None

        if not verify_password(password, account.password):
            return None

        session_id = uuid4()
        expires_at = datetime.now(timezone.utc) + timedelta(
            seconds=settings.session_expire_time
        )

        new_session = Session(
            id=session_id,
            account_id=account.id,
            expires_at=expires_at,
        )

        current_session = await self.session_repository.read_by_account_id(account.id)

        if current_session is not None:
            await self.session_repository.delete(current_session.id)

        success = await self.session_repository.create(new_session)

        if not success:
            return None

        return new_session

    async def delete_session(self, session_id: UUID) -> bool:
        return await self.session_repository.delete(session_id)

    async def validate_session(self, session_id: UUID) -> bool:
        session = await self.session_repository.read(session_id)

        if session is None:
            return False

        if session.expires_at < datetime.now(timezone.utc):
            return False

        return True

    async def get_account_from_session(self, session_id: UUID) -> Account | None:
        session = await self.session_repository.read(session_id)

        if session is None:
            return None

        if session.expires_at < datetime.now(timezone.utc):
            return None

        return await self.account_repository.read(session.account_id)
