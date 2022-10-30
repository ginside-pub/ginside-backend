from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from . import models, schemas
from .core.config import cfg


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str) -> schemas.UserInternal | bool:
    try:
        user = await models.user_get_internal(username)
    except models.UserDoesNotExistError:
        return False

    if not verify_password(password, user.password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta is not None:
        expire = datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=15)

    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(
        to_encode,
        cfg.security.secret_key,
        algorithm=cfg.security.hashing_algorithm,
    )

    return encoded_jwt


def decode_jwt_token(token: str) -> dict:
    return jwt.decode(token, cfg.security.secret_key, algorithms=[cfg.security.hashing_algorithm])


async def get_current_user(token: str = Depends(oauth2_scheme)) -> schemas.UserInternal:
    credentials_exception = HTTPException(
        status_code=401,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode_jwt_token(token)
        username: str = payload.get('sub')

        if not username:
            raise credentials_exception

        token_data = schemas.TokenData(username=username)
        user = await models.user_get(token_data.username)
    except JWTError as e:
        raise credentials_exception from e
    except models.UserDoesNotExistError as e:
        raise credentials_exception from e

    return user
