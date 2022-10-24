from datetime import datetime, timezone

from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import Table, Column, Integer, Text, DateTime

from .. import schemas
from ..core.postgres import get_session, metadata


Sample = Table(
    'sample',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Text, index=True, unique=True, nullable=False),
    Column('description', Text),
    Column('created_at', DateTime(timezone=True), nullable=False),
    Column('updated_at', DateTime(timezone=True)),
)


class SampleNameOccupiedError(Exception):
    """Raised on attempt to create a sample with occupied name."""


class SampleDoesNotExistError(Exception):
    """Raised on attempt to access a nonexistent sample."""


async def sample_create(sample: schemas.SampleCreate) -> schemas.SampleGet:
    query = Table.insert().values(
        sample.dict(), created_at=datetime.now(tz=timezone.utc),
    ).returning(*Sample.c)

    try:
        created = await get_session().fetch_one(query)
        return schemas.SampleGet(**created)
    except UniqueViolationError as e:
        raise SampleNameOccupiedError from e


async def sample_update(sample_id: int, sample: schemas.SampleUpdate) -> schemas.SampleGet:
    query = Table.update().where(Sample.c.id == sample_id).values(
        sample.dict(), updated_at=datetime.now(tz=timezone.utc),
    ).returning(*Sample.c)

    updated = await get_session().fetch_one(query)

    if not updated:
        raise SampleDoesNotExistError

    return schemas.SampleGet(**updated)


async def sample_get(sample_id: int) -> schemas.SampleGet:
    query = Table.select().where(Sample.c.id == sample_id)
    fetched = await get_session().fetch_one(query)

    if not fetched:
        raise SampleDoesNotExistError

    return schemas.SampleGet(**fetched)


async def sample_get_list() -> schemas.SampleGetList:
    query = Table.select()
    fetched = await get_session().fetch_all(query)
    return schemas.SampleGetList(samples=fetched)


async def sample_delete(sample_id: int):
    await sample_get(sample_id)
    query = Table.delete().where(Sample.c.id == sample_id)
    await get_session().execute(query)
