from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import crud
from ..core.security import create_access_token
from ..dependencies import get_db
from ..schemas.token import Token
from ..schemas.user import User
from ..dependencies import get_current_user
from ..models.user import User as UserModel

router = APIRouter()


@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db=db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")  # noqa: E501
    # elif not crud.user.is_active(user):
    #     raise HTTPException(status_code=401, detail="Inactive user")
    return {
        "access_token": create_access_token(sub=user.username),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=User)
def test_token(
    current_user: UserModel = Depends(get_current_user)
) -> Any:
    """
    Test access token
    """
    return current_user
