from fastapi import FastAPI

from .db.session import engine
from .exceptions import NotFoundError, not_found_error_handler
from .models import user as UserModel
from .routers import login, user

# create all tables that do not already exist
UserModel.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(login.router, tags=["login"])

app.add_exception_handler(NotFoundError, not_found_error_handler)
