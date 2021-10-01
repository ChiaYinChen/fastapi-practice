from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..crud import crud_user
from ..dependencies import get_db
from ..exceptions import NotFoundError
from ..schemas.user import User, UserCreate, UserUpdate

router = APIRouter()


@router.get("/{username}", response_model=User)
def get_user(
    username: str,
    db: Session = Depends(get_db)
):
    db_user = crud_user.get_user_by_username(db=db, username=username)
    if db_user is None:
        raise NotFoundError(message="User not found")
    return db_user


@router.post("/", response_model=User, status_code=201)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    db_user = crud_user.get_user_by_username(db=db, username=user.username)
    if db_user:
        return JSONResponse(
            status_code=400,
            content={"message": "User already exist"}
        )
    return crud_user.create_user(db=db, user=user)


@router.patch("/{username}")
def update_user(
    username: str,
    updates: UserUpdate,
    db: Session = Depends(get_db)
):
    db_user = crud_user.get_user_by_username(db=db, username=username)
    if db_user is None:
        raise NotFoundError(message="User not found")
    crud_user.update_user(db=db, db_obj=db_user, updates=updates)
    return JSONResponse(
        status_code=200,
        content={"message": "Update user success"}
    )


@router.delete("/{username}")
def delete_user(
    username: str,
    db: Session = Depends(get_db)
):
    db_user = crud_user.get_user_by_username(db=db, username=username)
    if db_user is None:
        raise NotFoundError(message="User not found")
    crud_user.delete_user(db=db, db_obj=db_user)
    return JSONResponse(
        status_code=200,
        content={"message": f"Deleted user {username}"}
    )
