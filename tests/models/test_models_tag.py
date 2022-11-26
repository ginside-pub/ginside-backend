from pytest import raises

from ginside import models, schemas


async def test_tag_create(postgres: None, tag_in_db: schemas.TagGet):
    await models.tag_create(post_id=tag_in_db.post_id, tag='new')
    tags = await models.tag_get_by_post(tag_in_db.post_id)
    assert tags.tags == [tag_in_db, schemas.TagGet(post_id=tag_in_db.post_id, tag='new')]


async def test_tag_create_existing(postgres: None, tag_in_db: schemas.TagGet):
    await models.tag_create(post_id=tag_in_db.post_id, tag=tag_in_db.tag)
    tags = await models.tag_get_by_post(tag_in_db.post_id)
    assert tags.tags == [tag_in_db]


async def test_tag_create_nonexistent_post(postgres: None):
    with raises(models.PostDoesNotExistError):
        await models.tag_create(post_id=0, tag='tag')


async def test_tag_get_by_post(postgres: None, tag_in_db: schemas.TagGet):
    fetched = await models.tag_get_by_post(tag_in_db.post_id)
    assert fetched.tags == [tag_in_db]


async def test_tag_delete(postgres: None, tag_in_db: schemas.TagGet):
    await models.tag_delete(tag_in_db.post_id, tag_in_db.tag)
