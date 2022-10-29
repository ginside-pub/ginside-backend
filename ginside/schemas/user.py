from datetime import datetime

from pydantic import BaseModel, validator

from .. import auth


class User(BaseModel):
    display_name: str | None
    bio: str | None


class UserCreate(User):
    username: str
    password: str

    @validator('password')
    def hash_password(cls, v: str):  # noqa: N805
        return auth.hash_password(v)


class UserUpdate(User):
    pass


class UserGet(User):
    username: str
    created_at: datetime


class UserGetList(BaseModel):
    users: list[UserGet]


class UserInternal(UserGet):
    password: str
