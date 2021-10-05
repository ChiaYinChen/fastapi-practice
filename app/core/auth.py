from typing import Optional

from sqlalchemy.orm.session import Session

from .. import crud
from ..models.user import User as UserModel
from ..core.security import verify_password


def authenticate(
    username: str,
    password: str,
    db: Session,
) -> Optional[UserModel]:
    user = crud.user.get_by_username(db=db, username=username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
