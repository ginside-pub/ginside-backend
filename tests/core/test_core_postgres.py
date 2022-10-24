from databases import Database
from pytest import raises
from pytest_mock import MockerFixture

from ginside.core import postgres
from ginside.core.config import cfg


async def test_postgres_session(mocker: MockerFixture):
    test_session = Database(cfg.database.get_url())
    database_mock = mocker.patch('databases.Database')
    database_mock.return_value = test_session

    with raises(postgres.PostgresNotConnectedError):
        postgres.get_session()

    await postgres.connect()
    database_mock.assert_called_once_with(
        cfg.database.get_url(),
        force_rollback=cfg.database.test,
    )
    assert postgres.get_session() == test_session

    await postgres.disconnect()
    with raises(postgres.PostgresNotConnectedError):
        postgres.get_session()
