from typing import Dict, Any

from async_asgi_testclient import TestClient
from pytest import fixture

from ginside import app


@fixture
async def api_client(postgres: None) -> TestClient:
    async with TestClient(app) as client:
        yield client


@fixture
async def auth_api_client(postgres: None) -> TestClient:
    async with TestClient(app) as client:
        resp = await client.post(
            '/auth/token',
            form={'username': 'jdoe', 'password': 'SECRET'},
        )
        token = resp.json()['access_token']

        client.headers = {'Authorization': f'Bearer {token}'}
        yield client


@fixture
def post_in_db() -> Dict[str, Any]:
    return {
        'id': 1,
        'title': 'First post',
        'contents': 'Contents of the post',
        'archived': False,
        'created_at': '2022-01-01T00:00:00+00:00',
        'updated_at': None,
    }


@fixture
def post_in_db_archived() -> Dict[str, Any]:
    return {
        'id': 2,
        'title': 'Archived post',
        'contents': 'Contents',
        'archived': True,
        'created_at': '2022-01-01T00:00:00+00:00',
        'updated_at': None,
    }


@fixture
def user_in_db() -> Dict[str, Any]:
    return {
        'username': 'jdoe',
        'display_name': 'John Doe',
        'bio': 'First user',
        'created_at': '2022-01-01T00:00:00+00:00',
    }
