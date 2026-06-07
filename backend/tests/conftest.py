import django
import pytest
from django.test import Client


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def admin_user(db):
    from restaurant.models import User
    user = User(username="admin@test.com", email="admin@test.com", first_name="Админ", is_staff=True)
    user.set_password("admin123")
    user.save()
    return user


@pytest.fixture
def regular_user(db):
    from restaurant.models import User
    user = User(username="user@test.com", email="user@test.com", first_name="Пользователь", is_staff=False)
    user.set_password("user123")
    user.save()
    return user


@pytest.fixture
def admin_token(client, admin_user):
    resp = client.post(
        "/api/auth/login",
        data={"email": "admin@test.com", "password": "admin123"},
        content_type="application/json",
    )
    return resp.json()["access_token"]


@pytest.fixture
def user_token(client, regular_user):
    resp = client.post(
        "/api/auth/login",
        data={"email": "user@test.com", "password": "user123"},
        content_type="application/json",
    )
    return resp.json()["access_token"]
