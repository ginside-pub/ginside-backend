from pytest import raises

from ginside import models, schemas


async def test_post_create(postgres: None):
    post = schemas.PostCreate(title='Post', contents='Lorem ipsum')
    created = await models.post_create(post, 'jdoe')

    assert created.title == post.title
    assert created.author == 'jdoe'
    assert created.contents == post.contents
    assert created.archived is False
    assert created.created_at is not None
    assert created.updated_at is None


async def test_post_create_nonexistent_author(postgres: None):
    post = schemas.PostCreate(title='Post', contents='Lorem ipsum')

    with raises(models.UserDoesNotExistError):
        await models.post_create(post, 'nonexistent')


async def test_post_get(postgres: None, post_in_db: schemas.PostGet):
    fetched = await models.post_get(post_in_db.id)
    assert fetched == post_in_db


async def test_post_get_list(postgres: None, post_in_db: schemas.PostGet):
    fetched = await models.post_get_list()
    assert fetched.posts == [post_in_db]

    post = schemas.PostCreate(title='Post', contents='Lorem ipsum')
    created = await models.post_create(post, 'jdoe')

    fetched = await models.post_get_list()
    assert fetched.posts == [post_in_db, created]


async def test_post_get_list_with_archived(
    postgres: None, post_in_db: schemas.PostGet, post_in_db_archived: schemas.PostGet,
):
    fetched = await models.post_get_list(include_archived=True)
    assert fetched.posts == [post_in_db, post_in_db_archived]


async def test_post_get_nonexistent(postgres: None):
    with raises(models.PostDoesNotExistError):
        await models.post_get(0)


async def test_post_update(postgres: None, post_in_db: schemas.PostGet):
    post = schemas.PostUpdate(contents='New contents', archived=True)
    updated = await models.post_update(post_in_db.id, post_in_db.author, post)

    assert updated.id == post_in_db.id
    assert updated.title == post_in_db.title
    assert updated.author == post_in_db.author
    assert updated.contents == 'New contents'
    assert updated.archived is True
    assert updated.created_at == post_in_db.created_at
    assert updated.updated_at is not None


async def test_post_update_nonexistent(postgres: None):
    post = schemas.PostUpdate(contents='New contents')

    with raises(models.PostDoesNotExistError):
        await models.post_update(0, 'jdoe', post)


async def test_post_delete(postgres: None, post_in_db: schemas.PostGet):
    await models.post_delete(post_in_db.id, post_in_db.author)

    with raises(models.PostDoesNotExistError):
        await models.post_get(post_in_db.id)


async def test_post_delete_nonexistent(postgres: None):
    with raises(models.PostDoesNotExistError):
        await models.post_delete(0, 'jdoe')
