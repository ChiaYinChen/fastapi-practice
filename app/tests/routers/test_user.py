"""User unit test."""
from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings


def test_get_user_me_by_normal(
    client: TestClient,
    normal_user_token_headers: Dict[str, str]
) -> None:
    """Test get_user_me with normal user."""
    r = client.get("/user/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
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
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is True
    assert current_user["username"] == settings.FIRST_SUPERUSER
    assert current_user["email"] == settings.FIRST_SUPERUSER_EMAIL
