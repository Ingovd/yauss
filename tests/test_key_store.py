import json

from key_store import *

def test_no_config():
    app = create_app()
    assert app

def test_request_10(key_store):
    client = key_store.test_client()
    response = client.get('/request/10')
    keys = json.loads(response.data)['keys']
    assert len(keys) == 10

def test_existing_key_not_approved(key_store):
    client = key_store.test_client()
    key_response = client.get('/request/1')
    key = json.loads(key_response.data)['keys'][0]
    approve_response = client.get(f'/approve/{key}')
    approved = json.loads(approve_response.data)['approved']
    assert not approved

def test_approve_inserts_key(key_store):
    client = key_store.test_client()
    response = client.get('/approve/abcdefgh')
    approved = json.loads(response.data)['approved']
    assert approved
    response = client.get(f'/approve/abcdefgh')
    approved = json.loads(response.data)['approved']
    assert not approved
