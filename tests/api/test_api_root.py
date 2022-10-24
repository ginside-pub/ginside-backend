from async_asgi_testclient import TestClient


async def test_redirect_to_docs(api_client: TestClient):
    resp = await api_client.get('/', allow_redirects=False)
    assert resp.status_code == 307
    assert 'location' in resp.headers and resp.headers['location'] == '/docs'
