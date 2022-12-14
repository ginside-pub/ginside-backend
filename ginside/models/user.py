from datetime import datetime, timezone

from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import Table, Column, Text, DateTime

from .. import schemas
from ..errors import UnreachableError
from ..core.postgres import get_session, metadata


User = Table(
    'users',
    metadata,
    Column('username', Text, primary_key=True),
    Column('password', Text, nullable=False),
    Column('display_name', Text, index=True, nullable=True),
    Column('bio', Text, nullable=True),
    Column('created_at', DateTime(timezone=True), nullable=False, index=True),
)


class UsernameOccupiedError(Exception):
    """Raised on attempt to use an occupied username."""


class UserDoesNotExistError(Exception):
    """Raised on attempt to access a nonexistent user."""


async def user_create(user: schemas.UserCreate) -> schemas.UserGet:
    query = User.insert().values(
        **user.dict(),
        created_at=datetime.now(tz=timezone.utc),
    ).returning(*User.c)

    try:
        created = await get_session().fetch_one(query)
    except UniqueViolationError:
        raise UsernameOccupiedError

    if created is None:  # pragma: no cover
        raise UnreachableError

    return schemas.UserGet(**created._mapping)


async def user_update(username: str, user: schemas.UserUpdate) -> schemas.UserGet:
    query = User.update().where(User.c.username == username).values(
        **user.dict(exclude_none=True)).returning(*User.c)

    updated = await get_session().fetch_one(query)

    if not updated:
        raise UserDoesNotExistError

    return schemas.UserGet(**updated._mapping)


async def user_get(username: str) -> schemas.UserGet:
    query = User.select().where(User.c.username == username)
    fetched = await get_session().fetch_one(query)

    if not fetched:
        raise UserDoesNotExistError

    return schemas.UserGet(**fetched._mapping)


async def user_get_internal(username: str) -> schemas.UserInternal:
    query = User.select().where(User.c.username == username)
    fetched = await get_session().fetch_one(query)

    if not fetched:
        raise UserDoesNotExistError

    return schemas.UserInternal(**fetched._mapping)


async def user_get_list() -> schemas.UserGetList:
    query = User.select()
    fetched = await get_session().fetch_all(query)
    return schemas.UserGetList(users=fetched)


async def user_delete(username: str):
    await user_get(username)
    query = User.delete().where(User.c.username == username)
    await get_session().execute(query)
