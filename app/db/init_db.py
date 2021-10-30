"""Initial db."""
import logging

from sqlalchemy.orm import Session

from .. import crud
from ..core.config import settings
from ..schemas.user import UserCreate

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    """Initialize super user."""
    user = crud.user.get_by_username(db=db, username=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            username=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        logger.info('Initial Super User')
        crud.user.create(db=db, obj_in=user_in)
    else:
        logger.warning(
            "Skipping creating superuser. User with username "
            f"`{settings.FIRST_SUPERUSER}` already exists. "
        )
