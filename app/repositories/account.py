import psycopg

from ..models import Account


class AccountRepository:
    def __init__(self, connection: psycopg.AsyncConnection):
        self.connection = connection

    async def get_account(self, account_id: int) -> Account:
        async with self.connection.cursor() as cursor:
            await cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
            record = await cursor.fetchone()
            return Account(
                id=record[0], username=record[1], password=record[2], email=record[3]
            )

    async def create_account(self, account: Account) -> Account:
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s) RETURNING id",
                (account.username, account.password, account.email),
            )
            account_id = await cursor.fetchone()
            return Account(
                id=account_id,
                username=account.username,
                password=account.password,
                email=account.email,
            )

    async def update_account(self, account: Account) -> Account:
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                "UPDATE accounts SET username = %s, password = %s, email = %s WHERE id = %s",
                (account.username, account.password, account.email, account.id),
            )
            return account

    async def delete_account(self, account_id: int):
        async with self.connection.cursor() as cursor:
            await cursor.execute("DELETE FROM accounts WHERE id = %s", (account_id,))
