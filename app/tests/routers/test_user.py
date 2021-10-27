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
    r = client.get("/user/me", headers=normal_user_token_headers)
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
    r = client.get("/user/me", headers=superuser_token_headers)
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
    r = client.get("/user/?skip=0&limit=100", headers=superuser_token_headers)
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
    r = client.get("/user/?skip=0&limit=100", headers=normal_user_token_headers)  # noqa: E501
    all_users = r.json()
    assert r.status_code == 401
    assert all_users == {"detail": "The user doesn't have enough privileges"}
