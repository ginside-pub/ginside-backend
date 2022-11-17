from typing import Any

from async_asgi_testclient import TestClient

from ginside import auth


async def test_get_me(auth_api_client: TestClient, user_in_db: dict[str, Any]):
    resp = await auth_api_client.get('/users/me')
    assert resp.status_code == 200
    assert resp.json() == user_in_db


async def test_get_me_unauthenticated(api_client: TestClient):
    resp = await api_client.get('/users/me')
    assert resp.status_code == 401
    assert resp.json()['detail'] == 'Not authenticated'


async def test_update_me(auth_api_client: TestClient, user_in_db: dict[str, Any]):
    resp = await auth_api_client.put('/users/me', json={'bio': 'New bio'})
    assert resp.status_code == 200
    assert resp.json() == {**user_in_db, 'bio': 'New bio'}


async def test_delete_me(auth_api_client: TestClient):
    resp = await auth_api_client.delete('/users/me')
    assert resp.status_code == 200
    resp = await auth_api_client.get('/users/me')
    assert resp.status_code == 401


async def test_get_user(api_client: TestClient, user_in_db: dict[str, Any]):
    resp = await api_client.get(f'/users/{user_in_db["username"]}')
    assert resp.status_code == 200
    assert resp.json() == user_in_db


async def test_get_user_nonexistent(api_client: TestClient):
    resp = await api_client.get('/users/nonexistent')
    assert resp.status_code == 404


async def test_get_users(
    api_client: TestClient,
    user_in_db: dict[str, Any],
    user_in_db_no_posts: dict[str, Any],
):
    resp = await api_client.get('/users/')
    assert resp.status_code == 200
    assert resp.json()['users'] == [user_in_db, user_in_db_no_posts]


async def test_create_user(api_client: TestClient):
    payload = {
        'username': 'jane',
        'password': 'JaneIsTotallyTheBest',
        'display_name': 'Jane Doe',
        'bio': 'A very humble girl from rural America.',
    }

    resp = await api_client.post('/users/', json=payload)
    assert resp.status_code == 200
    created = resp.json()

    for field in ['username', 'display_name', 'bio']:
        assert created[field] == payload[field]

    assert 'created_at' in created
    assert 'password' not in created

    authenticated = await auth.authenticate_user(payload['username'], payload['password'])
    assert authenticated.username == payload['username']


async def test_create_user_occupied_username(api_client: TestClient):
    resp = await api_client.post('/users/', json={'username': 'jdoe', 'password': 'assword'})
    assert resp.status_code == 400
