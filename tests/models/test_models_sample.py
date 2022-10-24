from pytest import raises

from ginside import models, schemas


async def test_sample_create(postgres: None):
    sample = schemas.SampleCreate(name='Sample', description='Lorem ipsum')
    created = await models.sample_create(sample)

    assert created.name == sample.name
    assert created.description == sample.description

    assert created.created_at is not None
    assert created.updated_at is None


async def test_sample_create_occupied_name(postgres: None):
    sample = schemas.SampleCreate(name='First')

    with raises(models.SampleNameOccupiedError):
        await models.sample_create(sample)


async def test_sample_get(postgres: None, sample_in_db: schemas.SampleGet):
    fetched = await models.sample_get(sample_in_db.id)
    assert fetched == sample_in_db


async def test_sample_get_list(postgres: None, sample_in_db: schemas.SampleGet):
    fetched = await models.sample_get_list()
    assert fetched.samples == [sample_in_db]

    sample = schemas.SampleCreate(name='Sample', description='Lorem ipsum')
    created = await models.sample_create(sample)

    fetched = await models.sample_get_list()
    assert fetched.samples == [sample_in_db, created]


async def test_sample_get_nonexistent(postgres: None):
    with raises(models.SampleDoesNotExistError):
        await models.sample_get(0)


async def test_sample_update(postgres: None, sample_in_db: schemas.SampleGet):
    sample = schemas.SampleUpdate(description='New description')
    updated = await models.sample_update(sample_in_db.id, sample)

    assert updated.id == sample_in_db.id
    assert updated.name == sample_in_db.name
    assert updated.created_at == sample_in_db.created_at
    assert updated.updated_at is not None


async def test_sample_update_nonexistent(postgres: None):
    sample = schemas.SampleUpdate(description='New description')

    with raises(models.SampleDoesNotExistError):
        await models.sample_update(0, sample)


async def test_sample_delete(postgres: None, sample_in_db: schemas.SampleGet):
    await models.sample_delete(sample_in_db.id)

    with raises(models.SampleDoesNotExistError):
        await models.sample_get(sample_in_db.id)


async def test_sample_delete_nonexistent(postgres: None):
    with raises(models.SampleDoesNotExistError):
        await models.sample_get(0)
