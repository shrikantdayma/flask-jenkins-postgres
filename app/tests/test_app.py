import os
import pytest
from app import get_db_connection, app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client

def test_index_route(monkeypatch, client):
    class DummyCursor:
        def execute(self, q):
            pass
        def fetchone(self):
            return ["PostgreSQL 13.3"]
        def close(self):
            pass

    class DummyConn:
        def cursor(self):
            return DummyCursor()
        def close(self):
            pass

    def dummy_connect(**kwargs):
        return DummyConn()

    monkeypatch.setattr("psycopg2.connect", dummy_connect)
    rv = client.get("/")
    assert rv.status_code == 200
    data = rv.get_json()
    assert "postgres_version" in data
    assert "PostgreSQL" in data["postgres_version"]

