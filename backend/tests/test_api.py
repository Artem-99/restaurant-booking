import pytest
from django.test import Client


@pytest.mark.django_db
def test_register(client):
    resp = client.post(
        "/api/auth/register",
        data={"email": "new@test.com", "password": "pass123", "first_name": "Иван"},
        content_type="application/json",
    )
    assert resp.status_code == 200
    assert resp.json()["email"] == "new@test.com"


@pytest.mark.django_db
def test_register_duplicate_email(client, regular_user):
    resp = client.post(
        "/api/auth/register",
        data={"email": "user@test.com", "password": "pass123", "first_name": "Иван"},
        content_type="application/json",
    )
    assert resp.status_code == 400


@pytest.mark.django_db
def test_login(client, regular_user):
    resp = client.post(
        "/api/auth/login",
        data={"email": "user@test.com", "password": "user123"},
        content_type="application/json",
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()


@pytest.mark.django_db
def test_login_wrong_password(client, regular_user):
    resp = client.post(
        "/api/auth/login",
        data={"email": "user@test.com", "password": "wrongpass"},
        content_type="application/json",
    )
    assert resp.status_code == 401


@pytest.mark.django_db
def test_me(client, user_token):
    resp = client.get("/api/auth/me", HTTP_AUTHORIZATION=f"Bearer {user_token}")
    assert resp.status_code == 200
    assert resp.json()["email"] == "user@test.com"


@pytest.mark.django_db
def test_list_tables(client):
    resp = client.get("/api/tables/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.django_db
def test_create_table_as_admin(client, admin_token):
    resp = client.post(
        "/api/tables/",
        data={"number": 1, "name": "У окна", "capacity": 4},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {admin_token}",
    )
    assert resp.status_code == 200
    assert resp.json()["number"] == 1


@pytest.mark.django_db
def test_create_table_as_user(client, user_token):
    resp = client.post(
        "/api/tables/",
        data={"number": 2, "name": "Угловой", "capacity": 2},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {user_token}",
    )
    assert resp.status_code == 403


@pytest.mark.django_db
def test_create_booking(client, user_token, admin_token):
    table_resp = client.post(
        "/api/tables/",
        data={"number": 1, "name": "У окна", "capacity": 4},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {admin_token}",
    )
    table_id = table_resp.json()["id"]
    resp = client.post(
        "/api/bookings/",
        data={"table_id": table_id, "date": "2026-12-01", "start_time": "12:00", "guests_count": 2},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {user_token}",
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "confirmed"


@pytest.mark.django_db
def test_double_booking(client, user_token, admin_token):
    table_resp = client.post(
        "/api/tables/",
        data={"number": 1, "name": "У окна", "capacity": 4},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {admin_token}",
    )
    table_id = table_resp.json()["id"]
    client.post(
        "/api/bookings/",
        data={"table_id": table_id, "date": "2026-12-01", "start_time": "12:00", "guests_count": 2},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {user_token}",
    )
    resp = client.post(
        "/api/bookings/",
        data={"table_id": table_id, "date": "2026-12-01", "start_time": "14:00", "guests_count": 1},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {user_token}",
    )
    assert resp.status_code == 409
