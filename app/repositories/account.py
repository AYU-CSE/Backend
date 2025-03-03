import psycopg

from ..models import Account


class AccountRepository:
    def __init__(self, connection: psycopg.AsyncConnection):
        self.connection = connection

    async def get_account(self, account_id: int) -> Account | None:
        async with self.connection.cursor() as cursor:
            await cursor.execute("SELECT * FROM account WHERE id = %s", (account_id,))
            record = await cursor.fetchone()

            if record is None:
                return None

            return Account(
                id=record[0],
                username=record[1],
                nickname=record[2],
                password=record[3],
                email=record[4],
                student_number=record[5],
            )

    async def get_account_by_username(self, username: str) -> Account | None:
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                "SELECT * FROM account WHERE username = %s", (username,)
            )
            record = await cursor.fetchone()

            if record is None:
                return None

            return Account(
                id=record[0],
                username=record[1],
                nickname=record[2],
                password=record[3],
                email=record[4],
                student_number=record[5],
            )

    async def create_account(self, account: Account) -> bool:
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO account (username, nickname, password, email, student_number) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (account.username, account.password, account.email),
            )

            if cursor.rowcount > 0:
                return True

            return False

    async def update_account(self, account: Account) -> bool:
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                "UPDATE account SET username = %s, nickname = %s, password = %s, email = %s, student_number = %s WHERE id = %s",
                (
                    account.username,
                    account.nickname,
                    account.password,
                    account.email,
                    account.student_number,
                    account.id,
                ),
            )

            if cursor.rowcount > 0:
                return True

            return False

    async def delete_account(self, account_id: int) -> bool:
        async with self.connection.cursor() as cursor:
            await cursor.execute("DELETE FROM account WHERE id = %s", (account_id,))

            if cursor.rowcount > 0:
                return True

            return False
