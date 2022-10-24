from uuid import uuid4

from databases import Database
from pytest import fixture
from pytest_mock import MockerFixture
from sqlalchemy import create_engine
from sqlalchemy_utils.functions import create_database, drop_database

from ginside import models  # noqa: F401
from ginside.core.config import cfg
from ginside.core.postgres import metadata


@fixture(autouse=True, scope='session')
def setup_db():
    old_db_name = cfg.database.database
    new_db_name = f'ginside-test-{uuid4()}'
    cfg.database.database = new_db_name
    db_url = cfg.database.get_url()

    try:
        create_database(db_url)
        engine = create_engine(db_url)
        metadata.create_all(engine)

        yield
    finally:
        drop_database(db_url)
        cfg.database.database = old_db_name


@fixture
async def postgres(mocker: MockerFixture):
    session: Database | None = None

    try:
        session = Database(cfg.database.get_url(), force_rollback=True)
        await session.connect()
        mocker.patch('ginside.core.postgres.get_session', return_value=session)

        yield
    finally:
        if session:
            await session.disconnect()
