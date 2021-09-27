from typing import Optional

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from exceptions import NotFoundError

app = FastAPI()


class UserBase(BaseModel):

    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None


class UserIn(UserBase):

    password: str = Field(..., min_length=5)


class UserOut(UserBase):

    pass


class UserInDB(UserBase):

    hashed_password: str


class UserUpdate(BaseModel):

    email: Optional[str] = None
    full_name: Optional[str] = None
    password: str = Field(None, min_length=5)


fake_db = {
    "ray": {
        "user_id": "a001",
        "username": "ray",
        "hashed_password": "supersecretraypass"
    },
    "will": {
        "user_id": "a002",
        "username": "will",
        "email": "will@gmail.com",
        "hashed_password": "supersecretwillpass"
    },
    "ted": {
        "user_id": "a003",
        "username": "ted",
        "email": "ted@gmail.com",
        "full_name": "ted ho",
        "hashed_password": "supersecrettedpass"
    },
}


@app.exception_handler(NotFoundError)
async def not_found_error_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user: UserBase, hashed_password: str):
    user_in_db = UserInDB(**user.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.get("/user/{username}")
async def get_user(username: str, response_model=UserOut):
    if username not in fake_db:
        raise NotFoundError(message="User not found")
    return fake_db[username]


@app.post("/user/", response_model=UserOut, status_code=201)
async def create_user(user_in: UserIn):
    if user_in.username in fake_db:
        return JSONResponse(
            status_code=400,
            content={"message": "User already exist"}
        )
    hashed_password = fake_password_hasher(user_in.password)
    user_saved = fake_save_user(user_in, hashed_password)
    fake_db[user_in.username] = jsonable_encoder(user_saved)
    return user_saved


@app.patch("/user/{username}", response_model=UserOut)
async def update_user(username: str, user_update: UserUpdate):
    if username not in fake_db:
        raise NotFoundError(message="User not found")
    stored_user_data = fake_db[username]
    stored_user_update_model = UserUpdate(**stored_user_data)
    update_data = user_update.dict(exclude_unset=True)
    updated_data = stored_user_update_model.copy(update=update_data)
    if updated_data.password:
        hashed_password = fake_password_hasher(
            raw_password=updated_data.password
        )
    else:
        hashed_password = stored_user_data["hashed_password"]
    user_saved = fake_save_user(
        user=UserBase(**updated_data.dict(), username=username),
        hashed_password=hashed_password
    )
    fake_db[username] = jsonable_encoder(user_saved)
    return user_saved


@app.delete("/user/{username}")
async def delete_user(username: str):
    if username not in fake_db:
        raise NotFoundError(message="User not found")
    fake_db.pop(username)
    return JSONResponse(
        status_code=200,
        content={"message": f"Deleted user {username}"}
    )
