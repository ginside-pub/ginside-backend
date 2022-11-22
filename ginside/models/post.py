from datetime import datetime, timezone

from asyncpg.exceptions import ForeignKeyViolationError
from sqlalchemy import Table, Column, Integer, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import and_

from .. import schemas
from ..core.postgres import get_session, metadata
from ..errors import UnreachableError
from .user import UserDoesNotExistError


Post = Table(
    'posts',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('author', Text, ForeignKey('users.username', ondelete='CASCADE'),
           nullable=False, index=True),
    Column('title', Text, index=True, nullable=False),
    Column('contents', Text, nullable=False),
    Column('archived', Boolean, nullable=False),
    Column('created_at', DateTime(timezone=True), nullable=False, index=True),
    Column('updated_at', DateTime(timezone=True)),
)


class PostDoesNotExistError(Exception):
    """Raised on attempt to access a nonexistent post."""


async def post_create(post: schemas.PostCreate, author: str) -> schemas.PostGet:
    query = Post.insert().values(
        **post.dict(),
        author=author,
        created_at=datetime.now(tz=timezone.utc),
    ).returning(*Post.c)

    try:
        created = await get_session().fetch_one(query)
    except ForeignKeyViolationError:
        raise UserDoesNotExistError

    if created is None:  # pragma: no cover
        raise UnreachableError

    return schemas.PostGet(**created._mapping)


async def post_update(post_id: int, author: str, post: schemas.PostUpdate) -> schemas.PostGet:
    query = Post.update().where(and_(Post.c.id == post_id, Post.c.author == author)).values(
        **post.dict(exclude_none=True),
        updated_at=datetime.now(tz=timezone.utc),
    ).returning(*Post.c)

    updated = await get_session().fetch_one(query)

    if not updated:
        raise PostDoesNotExistError

    return schemas.PostGet(**updated._mapping)


async def post_get(post_id: int) -> schemas.PostGet:
    query = Post.select().where(Post.c.id == post_id)
    fetched = await get_session().fetch_one(query)

    if not fetched:
        raise PostDoesNotExistError

    return schemas.PostGet(**fetched._mapping)


async def post_get_list(include_archived: bool = False) -> schemas.PostGetList:
    query = Post.select()

    if not include_archived:
        query = query.where(Post.c.archived.is_(False))

    fetched = await get_session().fetch_all(query)
    return schemas.PostGetList(posts=fetched)


async def post_delete(post_id: int, author: str):
    query = Post.delete().where(
        and_(Post.c.id == post_id, Post.c.author == author),
    ).returning(*Post.c)

    deleted = await get_session().fetch_one(query)

    if not deleted:
        raise PostDoesNotExistError
