import pytest
from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generate_aes():
    r = client.post("/keys/generate", json={"type":"AES"})
    assert r.status_code == 200
    data = r.json()
    assert data['key_type'] == 'AES'

def test_list_keys():
    r = client.get("/keys")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
