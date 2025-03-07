import psycopg

from ..models.account import Account, GetAccountDTO, UpdateAccountDTO
from ..repositories.account import AccountRepository
from ..utils.password import get_password_hash, identify_password


class AccountService:
    def __init__(self, connection: psycopg.AsyncConnection):
        self.connection = connection
        self.account_repository = AccountRepository(connection)

    async def get_account_by_id(self, account_id: int) -> GetAccountDTO | None:
        account = await self.account_repository.read(account_id)

        if account is None:
            return None

        return GetAccountDTO(**account.model_dump())

    async def create_account(self, account: Account) -> bool:
        if identify_password(account.password) is None:
            account.password = get_password_hash(account.password)

        return await self.account_repository.create(account)

    async def update_account(self, account_id: int, account: UpdateAccountDTO) -> bool:
        if identify_password(account.password) is None:
            account.password = get_password_hash(account.password)

        return await self.account_repository.update(
            account_id, account.model_dump(exclude_unset=True)
        )

    async def delete_account(self, account_id: int) -> bool:
        return await self.account_repository.delete(account_id)
