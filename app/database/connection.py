from psycopg_pool import AsyncConnectionPool

from ..config import SQL_CONFIG

pool: AsyncConnectionPool


def _get_connection_string() -> str:
    return (
        f"dbname={SQL_CONFIG['database']} "
        f"user={SQL_CONFIG['user']} "
        f"password={SQL_CONFIG['password']} "
        f"host={SQL_CONFIG['host']}"
    )


async def init_database():
    global pool
    pool = AsyncConnectionPool(_get_connection_string(), min_size=4, max_size=25)
    await pool.open()


async def close_database():
    await pool.close()


async def get_connection():
    async with pool.connection() as conn:
        yield conn
