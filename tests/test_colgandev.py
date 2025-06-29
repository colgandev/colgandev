import pytest
from fastapi.testclient import TestClient

from colgandev.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_system_boots():
    assert True
