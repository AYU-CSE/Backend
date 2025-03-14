import psycopg

from ..models.account import Account


class AccountRepository:
    def __init__(self, connection: psycopg.AsyncConnection):
        self.connection = connection

    async def read(self, account_id: int) -> Account | None:
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

    async def read_by_username(self, username: str) -> Account | None:
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

    async def create(self, account: Account) -> bool:
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO account (username, nickname, password, email, student_number) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (
                    account.username,
                    account.nickname,
                    account.password,
                    account.email,
                    account.student_number,
                ),
            )

            return cursor.rowcount > 0

    async def update(self, account_id: int, account: dict) -> bool:
        update_fields = []
        parameters = []

        for field, value in account.items():
            update_fields.append(f"{field} = %s")
            parameters.append(value)

        parameters.append(account_id)

        async with self.connection.cursor() as cursor:
            await cursor.execute(
                f"UPDATE account SET {', '.join(update_fields)} WHERE id = %s",
                parameters,
            )

            return cursor.rowcount > 0

    async def delete(self, account_id: int) -> bool:
        async with self.connection.cursor() as cursor:
            await cursor.execute("DELETE FROM account WHERE id = %s", (account_id,))

            return cursor.rowcount > 0
