from datetime import datetime, timezone

from sqlalchemy import Table, Column, Integer, Text, DateTime, Boolean

from .. import schemas
from ..core.postgres import get_session, metadata


Post = Table(
    'post',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', Text, index=True, nullable=False),
    Column('contents', Text, nullable=False),
    Column('archived', Boolean, default=False),
    Column('created_at', DateTime(timezone=True), nullable=False),
    Column('updated_at', DateTime(timezone=True)),
)


class PostDoesNotExistError(Exception):
    """Raised on attempt to access a nonexistent post."""


async def post_create(post: schemas.PostCreate) -> schemas.PostGet:
    query = Post.insert().values(
        **post.dict(),
        created_at=datetime.now(tz=timezone.utc),
    ).returning(*Post.c)

    created = await get_session().fetch_one(query)
    return schemas.PostGet(**created)


async def post_update(post_id: int, post: schemas.PostUpdate) -> schemas.PostGet:
    query = Post.update().where(Post.c.id == post_id).values(
        **post.dict(),
        updated_at=datetime.now(tz=timezone.utc),
    ).returning(*Post.c)

    updated = await get_session().fetch_one(query)

    if not updated:
        raise PostDoesNotExistError

    return schemas.PostGet(**updated)


async def post_get(post_id: int) -> schemas.PostGet:
    query = Post.select().where(Post.c.id == post_id)
    fetched = await get_session().fetch_one(query)

    if not fetched:
        raise PostDoesNotExistError

    return schemas.PostGet(**fetched)


async def post_get_list() -> schemas.PostGetList:
    query = Post.select()
    fetched = await get_session().fetch_all(query)
    return schemas.PostGetList(posts=fetched)


async def post_delete(post_id: int):
    await post_get(post_id)
    query = Post.delete().where(Post.c.id == post_id)
    await get_session().execute(query)
