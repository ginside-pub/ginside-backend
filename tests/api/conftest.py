from typing import Dict

from async_asgi_testclient import TestClient
from pytest import fixture

from ginside import app


@fixture
async def api_client(postgres: None) -> TestClient:
    async with TestClient(app) as client:
        yield client


@fixture
def sample_in_db() -> Dict[str, str]:
    return {
        'id': 1,
        'name': 'First',
        'description': 'Hello world!',
        'created_at': '2022-01-01T00:00:00+00:00',
        'updated_at': None,
    }
