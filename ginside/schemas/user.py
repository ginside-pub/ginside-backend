from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    display_name: str | None
    bio: str | None


class UserCreate(User):
    username: str


class UserUpdate(User):
    pass


class UserGet(UserCreate):
    created_at: datetime


class UserGetList(BaseModel):
    users: list[UserGet]
