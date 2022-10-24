from typing import Dict

from async_asgi_testclient import TestClient


async def test_sample_get(api_client: TestClient, sample_in_db: Dict[str, str]):
    resp = await api_client.get('/samples/')
    assert resp.status_code == 200
    assert resp.json() == {'samples': [sample_in_db]}


async def test_sample_get_by_id(api_client: TestClient, sample_in_db: Dict[str, str]):
    resp = await api_client.get(f'/samples/{sample_in_db["id"]}')
    assert resp.status_code == 200
    assert resp.json() == sample_in_db


async def test_sample_get_by_id_nonexistent(api_client: TestClient):
    sample_id = 0
    resp = await api_client.get(f'/samples/{sample_id}')
    assert resp.status_code == 404
    assert resp.json() == {'detail': f'Sample {sample_id!r} was not found.'}


async def test_sample_update(api_client: TestClient, sample_in_db: Dict[str, str]):
    description = 'Updated'
    resp = await api_client.put(f'/samples/{sample_in_db["id"]}', json={'description': description})
    assert resp.status_code == 200
    updated = resp.json()

    for field in ['id', 'name', 'created_at']:
        assert updated[field] == sample_in_db[field]

    assert updated['description'] == description
    assert updated['updated_at'] is not None


async def test_sample_update_nonexistent(api_client: TestClient):
    sample_id = 0
    resp = await api_client.put(f'/samples/{sample_id}', json={'description': None})
    assert resp.status_code == 404
    assert resp.json() == {'detail': f'Sample {sample_id!r} was not found.'}


async def test_sample_delete(api_client: TestClient, sample_in_db: Dict[str, str]):
    resp = await api_client.delete(f'/samples/{sample_in_db["id"]}')
    assert resp.status_code == 200
    resp = await api_client.get(f'/samples/{sample_in_db["id"]}')
    assert resp.status_code == 404


async def test_sample_delete_nonexistent(api_client: TestClient):
    sample_id = 0
    resp = await api_client.delete(f'/samples/{sample_id}')
    assert resp.status_code == 404
    assert resp.json() == {'detail': f'Sample {sample_id!r} was not found.'}


async def test_sample_create(api_client: TestClient):
    sample = {'name': 'New sample'}
    resp = await api_client.post('/samples/', json=sample)
    assert resp.status_code == 200

    created = resp.json()
    assert created['name'] == sample['name']
    assert created['description'] is None
    assert created['created_at'] is not None
    assert created['updated_at'] is None


async def test_sample_create_occupied_name(api_client: TestClient, sample_in_db: Dict[str, str]):
    resp = await api_client.post('/samples/', json={'name': sample_in_db['name']})
    assert resp.status_code == 400
    assert resp.json() == {'detail': f'Sample name {sample_in_db["name"]!r} is occupied.'}
