"""Crud user logic unit test."""
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.core.security import verify_password
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserUpdate


def test_create_user(db: Session) -> None:
    """Test for create user."""
    user = crud.user.get_by_username(
        db=db,
        username=settings.TEST_USER_USERNAME
    )
    if user:
        crud.user.remove(db=db, db_obj=user)
    user_in = UserCreate(
        username=settings.TEST_USER_USERNAME,
        email=settings.TEST_USER_EMAIL,
        password=settings.TEST_USER_PASSWORD
    )
    user = crud.user.create(db, obj_in=user_in)
    assert user.username == settings.TEST_USER_USERNAME
    assert user.email == settings.TEST_USER_EMAIL
    assert hasattr(user, "hashed_password")
    _test_check_if_user_is_active(db_obj=user)
    _test_check_if_user_is_superuser_normal_user(db_obj=user)


def _test_check_if_user_is_active(db_obj: UserModel) -> None:
    """Test for check if user is active."""
    is_active = crud.user.is_active(db_obj)
    assert is_active is True


def _test_check_if_user_is_superuser_normal_user(db_obj: UserModel) -> None:
    """Test for check if user is superuser (with normal user)."""
    is_superuser = crud.user.is_superuser(db_obj)
    assert is_superuser is False


def test_authenticate_user(db: Session) -> None:
    """Test for authenticate user."""
    authenticated_user = crud.user.authenticate(
        db=db,
        username=settings.TEST_USER_USERNAME,
        password=settings.TEST_USER_PASSWORD
    )
    assert authenticated_user
    assert settings.TEST_USER_EMAIL == authenticated_user.email


def test_authenticate_user_fail(db: Session) -> None:
    """Test for user authentication failure."""
    user = crud.user.authenticate(
        db=db,
        username="not_exist_user",
        password="not_exist_user_password"
    )
    assert user is None


def test_get_user(db: Session) -> None:
    """Test for get user."""
    user = crud.user.get_by_username(
        db=db,
        username=settings.TEST_USER_USERNAME
    )
    assert user
    assert user.email == settings.TEST_USER_EMAIL


def test_update_user(db: Session) -> None:
    """Test for update user."""
    user = crud.user.get_by_username(
        db=db, username=settings.TEST_USER_USERNAME
    )
    new_password = "newtestuserpass"
    user_in_update = UserUpdate(password=new_password)
    crud.user.update(db=db, db_obj=user, obj_in=user_in_update)
    user_2 = crud.user.get_by_username(
        db=db, username=settings.TEST_USER_USERNAME
    )
    assert user_2
    assert user.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)
