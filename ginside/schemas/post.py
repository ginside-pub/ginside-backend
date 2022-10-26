from datetime import datetime

from pydantic import BaseModel


class Post(BaseModel):
    title: str
    contents: str
    archived: bool = False


class PostCreate(Post):
    pass


class PostUpdate(Post):
    title: str | None
    contents: str | None
    archived: bool | None


class PostGet(PostCreate):
    id: int
    created_at: datetime
    updated_at: datetime | None


class PostGetList(BaseModel):
    posts: list[PostGet]