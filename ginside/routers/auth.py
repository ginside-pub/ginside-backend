from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .. import auth
from .. import schemas
from ..core.config import cfg
from ..responses import generate_responses


router = APIRouter()


@router.post(
    '/token',
    response_model=schemas.Token,
    responses=generate_responses(401),
)
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token_expires = timedelta(minutes=cfg.security.access_token_ttl)

    access_token = auth.create_access_token(
        data={'sub': user.username},
        expires_delta=access_token_expires,
    )

    return {'access_token': access_token, 'token_type': 'bearer'}
