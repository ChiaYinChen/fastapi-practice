from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .. import crud
from ..dependencies import get_db
from ..exceptions import NotFoundError
from ..schemas.user import User, UserCreate, UserUpdate

router = APIRouter()


@router.get("/{username}", response_model=User)
def get_user(
    username: str,
    db: Session = Depends(get_db)
):
    db_user = crud.user.get_by_username(db=db, username=username)
    if db_user is None:
        raise NotFoundError(message="User not found")
    return db_user


@router.post("/", response_model=User, status_code=201)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    db_user = crud.user.get_by_username(db=db, username=user_in.username)
    if db_user:
        return JSONResponse(
            status_code=400,
            content={"message": "User already exist"}
        )
    return crud.user.create(db=db, obj_in=user_in)


@router.patch("/{username}", response_model=User)
def update_user(
    username: str,
    user_in: UserUpdate,
    db: Session = Depends(get_db)
):
    db_user = crud.user.get_by_username(db=db, username=username)
    if db_user is None:
        raise NotFoundError(message="User not found")
    return crud.user.update(db=db, db_obj=db_user, obj_in=user_in)


@router.delete("/{username}")
def delete_user(
    username: str,
    db: Session = Depends(get_db)
):
    db_user = crud.user.get_by_username(db=db, username=username)
    if db_user is None:
        raise NotFoundError(message="User not found")
    removed_user = crud.user.remove(db=db, db_obj=db_user)
    return JSONResponse(
        status_code=200,
        content={"message": f"Deleted user {removed_user.username}"}
    )
