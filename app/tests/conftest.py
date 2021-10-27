"""Pytest's conftest.py."""
import logging
from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import color_formatter
from app.core.config import settings
from app.db.session import SessionLocal
from app.main import app
from .utils.user import authentication_token_from_username


@pytest.fixture(scope="session")
def db() -> Generator:
    """Postgres test session."""
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    """Mock client."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def normal_user_token_headers(
    client: TestClient,
    db: Session
) -> Dict[str, str]:
    """Token headers for normal user."""
    return authentication_token_from_username(
        client=client, username=settings.TEST_USER_USERNAME, db=db
    )


@pytest.fixture(scope='session', autouse=True)
def setup_logging():
    """Set custom logging handler for pytest."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    _handler = logging.StreamHandler()
    _handler.setFormatter(color_formatter)
    logger.addHandler(_handler)
