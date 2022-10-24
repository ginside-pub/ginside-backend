from datetime import datetime, timezone

from pytest import fixture

from ginside import schemas


@fixture
def sample_in_db():
    return schemas.SampleGet(
        id=1,
        name='First',
        description='Hello world!',
        created_at=datetime(2022, 1, 1, tzinfo=timezone.utc),
    )
