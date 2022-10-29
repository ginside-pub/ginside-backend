from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from . import models, schemas
from .core.config import cfg


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    try:
        user = await models.user_get(username)
    except models.UserDoesNotExistError:
        return False

    if not verify_password(password, user.password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(
        to_encode,
        cfg.security.secret_key,
        algorithm=cfg.security.hashing_algorithm,
    )

    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> schemas.UserInternal:
    credentials_exception = HTTPException(
        status_code=401,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(
            token,
            cfg.security.secret_key,
            algorithms=[cfg.security.hashing_algorithm],
        )

        username: str = payload.get('sub')

        if not username:
            raise credentials_exception

        token_data = schemas.TokenData(username=username)
    except JWTError as e:
        raise credentials_exception from e

    user = await models.user_get(token_data.username)

    if not user:
        raise credentials_exception

    return user
