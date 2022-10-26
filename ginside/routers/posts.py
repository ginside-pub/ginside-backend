from fastapi import APIRouter, HTTPException

from .. import models
from .. import schemas
from ..responses import generate_responses


router = APIRouter()


@router.get(
    '/',
    response_model=schemas.PostGetList,
    summary='Get list of all posts.',
)
async def posts_get(include_archived: bool = False):
    return await models.post_get_list(include_archived)


@router.get(
    '/{post_id}',
    response_model=schemas.PostGet,
    responses=generate_responses(404),
    summary='Get post by its ID.',
)
async def posts_get_by_id(post_id: int):
    """Retrieves post by its ID.

    Returns:
    - **404** if the post was not found.
    """

    try:
        return await models.post_get(post_id)
    except models.PostDoesNotExistError:
        raise HTTPException(status_code=404, detail=f'Post {post_id!r} was not found.')


@router.put(
    '/{post_id}',
    response_model=schemas.PostGet,
    responses=generate_responses(404),
    summary='Update post by its ID.',
)
async def posts_update(post_id: int, post: schemas.PostUpdate):
    """Updates post by its ID.

    Returns:
    - **404** if the post was not found.
    """

    try:
        return await models.post_update(post_id, post)
    except models.PostDoesNotExistError:
        raise HTTPException(status_code=404, detail=f'Post {post_id!r} was not found.')


@router.delete(
    '/{post_id}',
    responses=generate_responses(404),
    summary='Delete post by its ID.',
)
async def posts_delete(post_id: int):
    """Deletes post by its ID.

    Returns:
    - **404** if the post was not found.
    """

    try:
        await models.post_delete(post_id)
    except models.PostDoesNotExistError:
        raise HTTPException(status_code=404, detail=f'Post {post_id!r} was not found.')


@router.post(
    '/',
    response_model=schemas.PostGet,
    summary='Create post.',
)
async def posts_create(post: schemas.PostCreate):
    return await models.post_create(post)
