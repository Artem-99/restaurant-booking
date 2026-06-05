import pytest
from django.test import TestCase
from ninja.testing import TestClient
from config.urls import api


client = TestClient(api)


@pytest.mark.django_db
def test_register():
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "testpass123",
        "first_name": "Тест",
    })
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


@pytest.mark.django_db
def test_login_invalid():
    response = client.post("/auth/login", json={
        "email": "noone@example.com",
        "password": "wrong",
    })
    assert response.status_code == 401


@pytest.mark.django_db
def test_list_tables():
    response = client.get("/tables/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
