from fastapi import APIRouter, HTTPException

from .. import models
from .. import schemas
from ..responses import generate_responses


router = APIRouter()


@router.get(
    '/',
    response_model=schemas.SampleGetList,
    summary='Get list of all samples.',
)
async def samples_get():
    return await models.sample_get_list()


@router.get(
    '/{sample_id}',
    response_model=schemas.SampleGet,
    responses=generate_responses(404),
    summary='Get sample by its ID.',
)
async def samples_get_by_id(sample_id: int):
    """Retrieves sample by its ID.

    Returns:
    - **404** if the sample was not found.
    """

    try:
        return await models.sample_get(sample_id)
    except models.SampleDoesNotExistError:
        raise HTTPException(status_code=404, detail=f'Sample {sample_id!r} was not found.')


@router.put(
    '/{sample_id}',
    response_model=schemas.SampleGet,
    responses=generate_responses(404),
    summary='Update sample by its ID.',
)
async def samples_update(sample_id: int, sample: schemas.SampleUpdate):
    """Updates sample by its ID.

    Returns:
    - **404** if the sample was not found.
    """

    try:
        return await models.sample_update(sample_id, sample)
    except models.SampleDoesNotExistError:
        raise HTTPException(status_code=404, detail=f'Sample {sample_id!r} was not found.')


@router.delete(
    '/{sample_id}',
    responses=generate_responses(404),
    summary='Delete sample by its ID.',
)
async def samples_delete(sample_id: int):
    """Deletes sample by its ID.

    Returns:
    - **404** if the sample was not found.
    """

    try:
        await models.sample_delete(sample_id)
    except models.SampleDoesNotExistError:
        raise HTTPException(status_code=404, detail=f'Sample {sample_id!r} was not found.')


@router.post(
    '/',
    response_model=schemas.SampleGet,
    responses=generate_responses(400),
    summary='Create sample.',
)
async def samples_create(sample: schemas.SampleCreate):
    try:
        return await models.sample_create(sample)
    except models.SampleNameOccupiedError:
        raise HTTPException(status_code=400, detail=f'Sample name {sample.name!r} is occupied.')
