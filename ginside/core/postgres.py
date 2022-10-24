from sqlalchemy import MetaData
import databases

from .config import cfg


class PostgresNotConnectedError(Exception):
    """Raised on attempt to get nonexistent PostgreSQL session."""


metadata = MetaData()
session: databases.Database | None = None


async def connect() -> None:
    global session

    if not session:
        session = databases.Database(cfg.database.get_url(), force_rollback=cfg.test)
        await session.connect()


async def disconnect() -> None:
    global session

    if session:
        await session.disconnect()
        session = None


def get_session() -> databases.Database:
    global session

    if not session:
        raise PostgresNotConnectedError

    return session
