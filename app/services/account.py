import psycopg

from ..repositories import AccountRepository
from ..models import Account


class AccountService:
    def __init__(self, connection: psycopg.AsyncConnection):
        self.connection = connection
        self.account_repository = AccountRepository(connection)

    async def get_account(self, account_id: int) -> Account:
        return await self.account_repository.read(account_id)

    async def create_account(self, account) -> bool:
        return await self.account_repository.create(account)

    async def update_account(self, account) -> bool:
        return await self.account_repository.update(account)

    async def delete_account(self, account_id: int) -> bool:
        return await self.account_repository.delete(account_id)
