import psycopg

from ..models import Session


class SessionRepository:
    def __init__(self, connection: psycopg.AsyncConnection):
        self.connection = connection

    async def read(self, id: str) -> Session | None:
        async with self.connection.cursor() as cursor:
            await cursor.execute("SELECT * FROM session WHERE CAST(%s AS uuid)", (id,))
            record = await cursor.fetchone()

            if record is None:
                return None

            return Session(
                id=record[0],
                account_id=record[1],
                expires_at=record[2],
            )

    async def create(self, session: Session) -> bool:
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO session (id, account_id, expires_at) VALUES (%s, %s, %s)",
                (str(session.id), session.account_id, session.expires_at),
            )

            if cursor.rowcount > 0:
                return True

            return False

    async def update(self, session: Session) -> bool:
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                "UPDATE session SET account_id = %s, expires_at = %s WHERE id = %s",
                (session.account_id, session.expires_at, session.id),
            )

            if cursor.rowcount > 0:
                return True

            return False

    async def delete(self, id: str) -> bool:
        async with self.connection.cursor() as cursor:
            await cursor.execute("DELETE FROM session WHERE id = %s", (id,))

            if cursor.rowcount > 0:
                return True

            return False
