import json

def test_empty_db(key_store):
    client = key_store.test_client()
    response = client.get('/request/10')
    keys = json.loads(response.data)['keys']
    assert len(keys) == 10