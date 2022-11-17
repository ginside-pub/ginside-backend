from pytest import raises

from ginside import models, schemas


async def test_user_create(postgres: None):
    user = schemas.UserCreate(username='jane', password='secret', display_name='Jane Doe')
    created = await models.user_create(user)

    assert created.username == user.username
    assert created.display_name == user.display_name
    assert created.bio is None
    assert created.created_at is not None


async def test_user_create_with_occupied_username(postgres: None, user_in_db: schemas.UserGet):
    user = schemas.UserCreate(username=user_in_db.username, password='secret')

    with raises(models.UsernameOccupiedError):
        await models.user_create(user)


async def test_user_get(postgres: None, user_in_db: schemas.UserGet):
    fetched = await models.user_get(user_in_db.username)
    assert fetched == user_in_db


async def test_user_get_list(
    postgres: None, user_in_db: schemas.UserGet, user_in_db_no_posts: schemas.UserGet,
):
    fetched = await models.user_get_list()
    assert fetched.users == [user_in_db, user_in_db_no_posts]

    user = schemas.UserCreate(username='jane', password='secret')
    created = await models.user_create(user)

    fetched = await models.user_get_list()
    assert fetched.users == [user_in_db, user_in_db_no_posts, created]


async def test_user_get_nonexistent(postgres: None):
    with raises(models.UserDoesNotExistError):
        await models.user_get('nonexistent')


async def test_user_update(postgres: None, user_in_db: schemas.UserGet):
    user = schemas.UserUpdate(display_name='Johnny', bio='Sins')
    updated = await models.user_update(user_in_db.username, user)

    assert updated.username == user_in_db.username
    assert updated.display_name == user.display_name
    assert updated.bio == user.bio
    assert updated.created_at == user_in_db.created_at


async def test_user_update_nonexistent(postgres: None):
    user = schemas.UserUpdate(display_name='...')

    with raises(models.UserDoesNotExistError):
        await models.user_update('nonexistent', user)


async def test_user_delete(postgres: None, user_in_db: schemas.UserGet):
    await models.user_delete(user_in_db.username)

    with raises(models.UserDoesNotExistError):
        await models.user_get(user_in_db.username)


async def test_user_delete_nonexistent(postgres: None):
    with raises(models.UserDoesNotExistError):
        await models.user_delete('nonexistent')
