from typing import Dict

from async_asgi_testclient import TestClient


async def test_post_get(api_client: TestClient, post_in_db: Dict[str, str]):
    resp = await api_client.get('/posts/')
    assert resp.status_code == 200
    assert resp.json() == {'posts': [post_in_db]}


async def test_post_get_by_id(api_client: TestClient, post_in_db: Dict[str, str]):
    resp = await api_client.get(f'/posts/{post_in_db["id"]}')
    assert resp.status_code == 200
    assert resp.json() == post_in_db


async def test_post_get_by_id_nonexistent(api_client: TestClient):
    post_id = 0
    resp = await api_client.get(f'/posts/{post_id}')
    assert resp.status_code == 404
    assert resp.json() == {'detail': f'Post {post_id!r} was not found.'}


async def test_post_update(api_client: TestClient, post_in_db: Dict[str, str]):
    contents = 'Updated'
    resp = await api_client.put(f'/posts/{post_in_db["id"]}', json={'contents': contents})
    assert resp.status_code == 200
    updated = resp.json()

    for field in ['id', 'title', 'archived', 'created_at']:
        assert updated[field] == post_in_db[field]

    assert updated['contents'] == contents
    assert updated['updated_at'] is not None


async def test_post_update_nonexistent(api_client: TestClient):
    post_id = 0
    resp = await api_client.put(f'/posts/{post_id}', json={'contents': 'New contents'})
    assert resp.status_code == 404
    assert resp.json() == {'detail': f'Post {post_id!r} was not found.'}


async def test_post_delete(api_client: TestClient, post_in_db: Dict[str, str]):
    resp = await api_client.delete(f'/posts/{post_in_db["id"]}')
    assert resp.status_code == 200
    resp = await api_client.get(f'/posts/{post_in_db["id"]}')
    assert resp.status_code == 404


async def test_post_delete_nonexistent(api_client: TestClient):
    post_id = 0
    resp = await api_client.delete(f'/posts/{post_id}')
    assert resp.status_code == 404
    assert resp.json() == {'detail': f'Post {post_id!r} was not found.'}


async def test_post_create(api_client: TestClient):
    post = {'title': 'New post', 'contents': 'Contents', 'archived': True}
    resp = await api_client.post('/posts/', json=post)
    assert resp.status_code == 200

    created = resp.json()
    assert created['title'] == post['title']
    assert created['contents'] == post['contents']
    assert created['archived'] == post['archived']
    assert created['created_at'] is not None
    assert created['updated_at'] is None
