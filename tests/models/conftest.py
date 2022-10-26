from datetime import datetime, timezone

from pytest import fixture

from ginside import schemas


@fixture
def post_in_db():
    return schemas.PostGet(
        id=1,
        title='First post',
        contents='Contents of the post',
        archived=False,
        created_at=datetime(2022, 1, 1, tzinfo=timezone.utc),
        updated_at=None,
    )
