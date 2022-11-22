from datetime import timedelta
from time import sleep

from fastapi import HTTPException
from jose import JWTError
from pytest import raises

from ginside import auth


def test_password_hashing():
    password = 'my_secret_password'
    hashed = auth.hash_password(password)
    assert auth.verify_password(password, hashed) is True
    assert auth.verify_password('wrong', hashed) is False


async def test_authenticate_user(postgres: None):
    authenticated_user = await auth.authenticate_user('jdoe', 'SECRET')
    assert authenticated_user.display_name == 'John Doe'


async def test_authenticate_nonexistent_user(postgres: None):
    with raises(auth.InvalidCredentialsError):
        await auth.authenticate_user('nonexistent', 'password')


async def test_authenticate_user_wrong_password(postgres: None):
    with raises(auth.InvalidCredentialsError):
        await auth.authenticate_user('jdoe', 'password')


def test_access_token():
    payload = {'one': 1, 'two': 2}
    encoded = auth.create_access_token(payload)
    decoded = auth.decode_jwt_token(encoded)
    assert decoded['exp'] is not None
    assert decoded['one'] == payload['one']
    assert decoded['two'] == payload['two']


def test_access_token_expired():
    encoded = auth.create_access_token({}, timedelta(seconds=0))
    sleep(1)

    with raises(JWTError):
        auth.decode_jwt_token(encoded)


def test_access_token_invalid():
    with raises(JWTError):
        auth.decode_jwt_token('Invalid token')


async def test_get_current_user(postgres: None):
    token = auth.create_access_token({'sub': 'jdoe'})
    user = await auth.get_current_user(token)
    assert user.username == 'jdoe'


async def test_get_current_user_without_username(postgres: None):
    token = auth.create_access_token({})

    with raises(HTTPException):
        await auth.get_current_user(token)


async def test_get_current_user_invalid_token(postgres: None):
    with raises(HTTPException):
        await auth.get_current_user('Invalid token')


async def test_get_current_user_nonexistent(postgres: None):
    token = auth.create_access_token({'sub': 'nonexistent'})

    with raises(HTTPException):
        await auth.get_current_user(token)
