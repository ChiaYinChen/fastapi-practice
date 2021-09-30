from typing import List

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .crud import crud_user
from .db.sqlite import engine
from .dependencies import get_db
from .exceptions import NotFoundError
from .models import user as UserModel
from .schemas.user import User, UserCreate, UserUpdate

# https://stackoverflow.com/a/68383073
UserModel.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.exception_handler(NotFoundError)
async def not_found_error_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


@app.get("/user/{username}", response_model=User)
def get_user(
    username: str,
    db: Session = Depends(get_db)
):
    db_user = crud_user.get_user_by_username(db=db, username=username)
    if db_user is None:
        raise NotFoundError(message="User not found")
    return db_user


@app.get("/users/", response_model=List[User])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    users = crud_user.get_users(db=db, skip=skip, limit=limit)
    return users


@app.post("/user/", response_model=User, status_code=201)
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


@app.patch("/user/{username}")
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


@app.delete("/user/{username}")
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
