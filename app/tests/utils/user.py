"""Util function for unit test."""
from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate, UserUpdate


def user_authentication_headers(
    client: TestClient, username: str, password: str
) -> Dict[str, str]:
    """Obtain user access_token."""
    data = {"username": username, "password": password}

    r = client.post("/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_username(
    client: TestClient, username: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given username.

    If the user doesn't exist it is created first.
    """
    password = settings.TEST_USER_PASSWORD
    db_user = crud.user.get_by_username(db=db, username=username)
    if not db_user:
        user_in_create = UserCreate(username=username, email=settings.TEST_USER_EMAIL, password=password)  # noqa: E501
        crud.user.create(db=db, obj_in=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        crud.user.update(db=db, db_obj=db_user, obj_in=user_in_update)

    return user_authentication_headers(client=client, username=username, password=password)  # noqa: E501
