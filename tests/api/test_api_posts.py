from typing import Dict, Any

from async_asgi_testclient import TestClient


async def test_post_get(api_client: TestClient, post_in_db: Dict[str, Any]):
    resp = await api_client.get('/posts/')
    assert resp.status_code == 200
    assert resp.json() == {'posts': [post_in_db]}


async def test_post_get_with_archived(
    api_client: TestClient, post_in_db: Dict[str, Any], post_in_db_archived: Dict[str, Any],
):
    resp = await api_client.get('/posts/?include_archived=true')
    assert resp.status_code == 200
    assert resp.json() == {'posts': [post_in_db, post_in_db_archived]}


async def test_post_get_by_id(api_client: TestClient, post_in_db: Dict[str, Any]):
    resp = await api_client.get(f'/posts/{post_in_db["id"]}')
    assert resp.status_code == 200
    assert resp.json() == post_in_db


async def test_post_get_by_id_nonexistent(api_client: TestClient):
    post_id = 0
    resp = await api_client.get(f'/posts/{post_id}')
    assert resp.status_code == 404
    assert resp.json() == {'detail': f'Post {post_id!r} was not found.'}


async def test_post_update(auth_api_client: TestClient, post_in_db: Dict[str, Any]):
    contents = 'Updated'
    resp = await auth_api_client.put(f'/posts/{post_in_db["id"]}', json={'contents': contents})
    assert resp.status_code == 200
    updated = resp.json()

    for field in ['id', 'title', 'archived', 'created_at']:
        assert updated[field] == post_in_db[field]

    assert updated['contents'] == contents
    assert updated['updated_at'] is not None


async def test_post_update_nonexistent(auth_api_client: TestClient):
    post_id = 0
    resp = await auth_api_client.put(f'/posts/{post_id}', json={'contents': 'New contents'})
    assert resp.status_code == 404
    assert resp.json() == {'detail': f'Post {post_id!r} was not found.'}


async def test_post_delete(auth_api_client: TestClient, post_in_db: Dict[str, Any]):
    resp = await auth_api_client.delete(f'/posts/{post_in_db["id"]}')
    assert resp.status_code == 200
    resp = await auth_api_client.get(f'/posts/{post_in_db["id"]}')
    assert resp.status_code == 404


async def test_post_delete_nonexistent(auth_api_client: TestClient):
    post_id = 0
    resp = await auth_api_client.delete(f'/posts/{post_id}')
    assert resp.status_code == 404
    assert resp.json() == {'detail': f'Post {post_id!r} was not found.'}


async def test_create_post(auth_api_client: TestClient):
    post = {'title': 'New post', 'contents': 'Contents', 'archived': True}
    resp = await auth_api_client.post('/posts/', json=post)
    assert resp.status_code == 200

    created = resp.json()
    assert created['title'] == post['title']
    assert created['author'] == 'jdoe'
    assert created['contents'] == post['contents']
    assert created['archived'] == post['archived']
    assert created['created_at'] is not None
    assert created['updated_at'] is None
