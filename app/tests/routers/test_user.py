"""User unit test."""
import logging
from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings


logger = logging.getLogger(__name__)


def test_get_user_me_by_normal(
    client: TestClient,
    normal_user_token_headers: Dict[str, str]
) -> None:
    """Test get_user_me with normal user."""
    r = client.get("/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["username"] == settings.TEST_USER_USERNAME
    assert current_user["email"] == settings.TEST_USER_EMAIL


def test_get_user_me_by_superuser(
    client: TestClient,
    superuser_token_headers: Dict[str, str]
) -> None:
    """Test get_user_me with superuser."""
    r = client.get("/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is True
    assert current_user["username"] == settings.FIRST_SUPERUSER
    assert current_user["email"] == settings.FIRST_SUPERUSER_EMAIL


def test_get_users_by_superuser(
    client: TestClient,
    superuser_token_headers: Dict[str, str]
) -> None:
    """Test get_users with superuser."""
    r = client.get("/users/?skip=0&limit=100", headers=superuser_token_headers)
    all_users = r.json()
    logger.debug(f"Total get {len(all_users)} users.")
    assert r.status_code == 200
    assert isinstance(all_users, list)
    assert len(all_users) > 0


def test_get_users_by_normal(
    client: TestClient,
    normal_user_token_headers: Dict[str, str]
) -> None:
    """Test get_users with normal user."""
    r = client.get("/users/?skip=0&limit=100", headers=normal_user_token_headers)  # noqa: E501
    all_users = r.json()
    assert r.status_code == 401
    assert all_users == {"detail": "The user doesn't have enough privileges"}


def test_get_user(
    client: TestClient
) -> None:
    """Test get_user (existing user)."""
    r = client.get(f"/users/{settings.TEST_USER_USERNAME}")
    api_user = r.json()
    assert r.status_code == 200
    assert isinstance(api_user, dict)
    assert api_user["username"] == settings.TEST_USER_USERNAME
    assert api_user["email"] == settings.TEST_USER_EMAIL


def test_get_user_not_exist(
    client: TestClient
) -> None:
    """Test get_user (user not exist)."""
    r = client.get("/users/not_exist_user")
    api_user = r.json()
    assert r.status_code == 404
    assert api_user == {"message": "User not found"}


def test_create_exist_user(
    client: TestClient
) -> None:
    """Test create_user (existing user)."""
    data = {
        "username": settings.TEST_USER_USERNAME,
        "email": settings.TEST_USER_EMAIL,
        "password": settings.TEST_USER_PASSWORD
    }
    r = client.post("/users/", json=data)
    created_user = r.json()
    assert r.status_code == 400
    assert created_user == {"message": "User already exist"}


def test_update_user_not_exist(
    client: TestClient
) -> None:
    """Test update_user (user not exist)."""
    data = {"email": "not_found@example.com"}
    r = client.patch("/users/not_exist_user", json=data)
    created_user = r.json()
    assert r.status_code == 404
    assert created_user == {"message": "User not found"}


def test_delete_user_not_exist(
    client: TestClient
) -> None:
    """Test delete_user (user not exist)."""
    r = client.delete("/users/not_exist_user")
    created_user = r.json()
    assert r.status_code == 404
    assert created_user == {"message": "User not found"}
