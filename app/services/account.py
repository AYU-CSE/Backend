import psycopg

from ..repositories.account import AccountRepository
from ..models.account import Account
from ..utils.password import identify_password, get_password_hash


class AccountService:
    def __init__(self, connection: psycopg.AsyncConnection):
        self.connection = connection
        self.account_repository = AccountRepository(connection)

    async def get_account_by_id(self, account_id: int) -> Account | None:
        return await self.account_repository.read(account_id)

    async def create_account(self, account: Account) -> bool:
        if identify_password(account.password) is None:
            account.password = get_password_hash(account.password)

        return await self.account_repository.create(account)

    async def update_account(self, account: Account) -> bool:
        if identify_password(account.password) is None:
            account.password = get_password_hash(account.password)

        return await self.account_repository.update(account)

    async def delete_account(self, account: Account) -> bool:
        return await self.account_repository.delete(account.id)
