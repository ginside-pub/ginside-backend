from async_asgi_testclient import TestClient

from ginside import auth


async def test_obtain_token(api_client: TestClient):
    resp = await api_client.post(
        '/auth/token',
        form={'username': 'jdoe', 'password': 'SECRET'},
    )

    token = resp.json()['access_token']
    user = await auth.get_current_user(token)
    assert user.username == 'jdoe'


async def test_obtain_token_incorrect_credentials(api_client: TestClient):
    resp = await api_client.post(
        '/auth/token',
        form={'username': 'jdoe', 'password': 'WRONG'},
    )

    assert resp.status_code == 401
    assert resp.json()['detail'] == 'Incorrect username or password'


async def test_get_current_user(auth_api_client: TestClient):
    resp = await auth_api_client.get('/auth/me')
    assert resp.status_code == 200
    fetched = resp.json()
    assert fetched['username'] == 'jdoe'
    assert 'password' not in fetched


async def test_get_current_user_unauthenticated(api_client: TestClient):
    resp = await api_client.get('/auth/me')
    assert resp.status_code == 401
    assert resp.json()['detail'] == 'Not authenticated'
