from fastapi import APIRouter, HTTPException, Depends

from .. import models, schemas, auth
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
async def posts_update(
    post_id: int,
    post: schemas.PostUpdate,
    current_user: schemas.UserInternal = Depends(auth.get_current_user),
):
    """Updates post by its ID.

    Returns:
    - **404** if the post was not found.
    """

    try:
        return await models.post_update(post_id, current_user.username, post)
    except models.PostDoesNotExistError:
        raise HTTPException(status_code=404, detail=f'Post {post_id!r} was not found.')


@router.delete(
    '/{post_id}',
    responses=generate_responses(404),
    summary='Delete post by its ID.',
)
async def posts_delete(
    post_id: int,
    current_user: schemas.UserInternal = Depends(auth.get_current_user),
):
    """Deletes post by its ID.

    Returns:
    - **404** if the post was not found.
    """

    try:
        await models.post_delete(post_id, current_user.username)
    except models.PostDoesNotExistError:
        raise HTTPException(status_code=404, detail=f'Post {post_id!r} was not found.')


@router.post(
    '/',
    response_model=schemas.PostGet,
    summary='Create post.',
)
async def posts_create(
    post: schemas.PostCreate,
    current_user: schemas.UserInternal = Depends(auth.get_current_user),
):
    return await models.post_create(post, current_user.username)
