from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..crud import crud_user
from ..dependencies import get_db
from ..schemas.user import User

router = APIRouter()


@router.get("/", response_model=List[User])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    users = crud_user.get_users(db=db, skip=skip, limit=limit)
    return users
