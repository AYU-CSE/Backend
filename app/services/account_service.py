import psycopg

from ..repositories import AccountRepository


class AccountService:
    def __init__(self, connection: psycopg.Connection):
        self.connection = connection
        self.account_repository = AccountRepository(connection)

    async def get_account(self, account_id: int):
        return await self.account_repository.get_account(account_id)

    async def create_account(self, account):
        return await self.account_repository.create_account(account)

    async def update_account(self, account):
        return await self.account_repository.update_account(account)

    async def delete_account(self, account_id: int):
        return await self.account_repository.delete_account(account_id)
