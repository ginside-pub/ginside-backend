from fastapi import APIRouter, HTTPException, Depends

from .. import models, schemas, auth
from ..responses import generate_responses


router = APIRouter()


@router.post(
    '/',
    response_model=schemas.UserGet,
    responses=generate_responses(400),
    summary='Create user.',
)
async def users_create(user: schemas.UserCreate):
    """Create a new user.

    Returns:
    - **400** if the username is already occupied.
    """

    try:
        return await models.user_create(user)
    except models.UsernameOccupiedError as e:
        raise HTTPException(
            status_code=400,
            detail=f'Username {user.username!r} is already occupied.',
        ) from e


@router.get(
    '/',
    response_model=schemas.UserGetList,
    summary='Get list of all users.',
)
async def users_get():
    return await models.user_get_list()


@router.get(
    '/me',
    response_model=schemas.UserGet,
    summary='Get currently authenticated user.',
)
async def users_get_me(current_user: schemas.UserInternal = Depends(auth.get_current_user)):
    return await models.user_get(current_user.username)


@router.put(
    '/me',
    response_model=schemas.UserGet,
    summary='Update currently authenticated user.',
)
async def users_update_me(
    user: schemas.UserUpdate,
    current_user: schemas.UserInternal = Depends(auth.get_current_user),
):
    return await models.user_update(current_user.username, user)


@router.delete(
    '/me',
    summary='Delete currently authenticated user.',
)
async def users_delete(current_user: schemas.UserInternal = Depends(auth.get_current_user)):
    await models.user_delete(current_user.username)


@router.get(
    '/{username}',
    response_model=schemas.UserGet,
    responses=generate_responses(404),
    summary='Get user by their username.',
)
async def users_get_by_id(username: str):
    """Retrieves user by their username.

    Returns:
    - **404** if the user was not found.
    """

    try:
        return await models.user_get(username)
    except models.UserDoesNotExistError:
        raise HTTPException(status_code=404, detail=f'User {username!r} was not found.')
