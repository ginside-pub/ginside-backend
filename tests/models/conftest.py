from datetime import datetime, timezone

from pytest import fixture

from ginside import schemas


@fixture
def post_in_db():
    return schemas.PostGet(
        id=1,
        author='jdoe',
        title='First post',
        contents='Contents of the post',
        archived=False,
        created_at=datetime(2022, 1, 1, tzinfo=timezone.utc),
        updated_at=None,
    )


@fixture
def post_in_db_archived():
    return schemas.PostGet(
        id=2,
        author='jdoe',
        title='Archived post',
        contents='Contents',
        archived=True,
        created_at=datetime(2022, 1, 1, tzinfo=timezone.utc),
        updated_at=None,
    )


@fixture
def tag_in_db():
    return schemas.TagGet(post_id=1, tag='tag')


@fixture
def user_in_db():
    return schemas.UserGet(
        username='jdoe',
        display_name='John Doe',
        bio='First user',
        created_at=datetime(2022, 1, 1, tzinfo=timezone.utc),
    )


@fixture
def user_in_db_no_posts():
    return schemas.UserGet(
        username='jack',
        display_name='Jack Doe',
        bio='No posts',
        created_at=datetime(2022, 1, 1, tzinfo=timezone.utc),
    )
