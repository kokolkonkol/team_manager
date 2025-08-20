import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.crud import DatabaseConnection

class TestDatabase(DatabaseConnection):
    def __init__(self):
        super().__init__(":memory:")
        self._init_db()

    def _init_db(self):
        with self.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """)
            cursor.execute("DELETE FROM employees")
            cursor.execute("INSERT INTO employees (name) VALUES (?)", ("Test Employee",))
            self.commit()

@pytest.fixture(scope="function")
def test_db():
    db = TestDatabase()
    yield db
    db.close()

@pytest.fixture(scope="function")
def client(test_db):
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()