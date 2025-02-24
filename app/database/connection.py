from psycopg_pool import AsyncConnectionPool

from ..config import settings

pool: AsyncConnectionPool


async def init_database():
    global pool
    pool = AsyncConnectionPool(
        settings.postgres_dsn.unicode_string(), min_size=4, max_size=25
    )
    await pool.open()


async def close_database():
    await pool.close()


async def get_connection():
    async with pool.connection() as conn:
        yield conn
