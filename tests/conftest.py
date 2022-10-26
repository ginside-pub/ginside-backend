from uuid import uuid4

from pytest import fixture
from pytest_mock import MockerFixture
from sqlalchemy import create_engine
from sqlalchemy_utils.functions import create_database, drop_database

from ginside import models  # noqa: F401
from ginside.core.postgres import metadata, connect, disconnect
from ginside.core.config import cfg


@fixture(autouse=True, scope='session')
def setup_db():
    cfg.database.test = True

    old_db_name = cfg.database.database
    new_db_name = f'ginside-test-{uuid4()}'
    cfg.database.database = new_db_name
    db_url = cfg.database.get_url()

    try:
        create_database(db_url)
        engine = create_engine(db_url)
        metadata.create_all(engine)

        with engine.connect() as connection:
            connection.execute("""
              INSERT INTO post (archived, title, contents, created_at)
              VALUES (FALSE, 'First post', 'Contents of the post', '2022-01-01T00:00:00+00:00');
            """)

        yield
    finally:
        cfg.database.database = old_db_name
        drop_database(db_url)


@fixture
async def postgres(mocker: MockerFixture):
    try:
        await connect()
        yield
    finally:
        await disconnect()
