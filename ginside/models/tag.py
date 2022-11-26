from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from sqlalchemy import Table, Column, Integer, Text, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.sql import and_

from .. import schemas
from ..core.postgres import get_session, metadata
from .post import PostDoesNotExistError


Tag = Table(
    'tags',
    metadata,
    Column('post_id', Integer, ForeignKey('posts.id', ondelete='CASCADE'),
           index=True, nullable=False),
    Column('tag', Text, index=True, nullable=False),
    PrimaryKeyConstraint('post_id', 'tag', name='tags_pk'),
)


async def tag_create(post_id: int, tag: str):
    query = Tag.insert().values(post_id=post_id, tag=tag)

    transaction = await get_session().transaction()

    try:
        await get_session().execute(query)
    except ForeignKeyViolationError as e:
        await transaction.rollback()
        raise PostDoesNotExistError from e
    except UniqueViolationError:
        await transaction.rollback()
    else:
        await transaction.commit()


async def tag_get_by_post(post_id: int) -> schemas.TagGetList:
    query = Tag.select().where(Tag.c.post_id == post_id)
    tags = await get_session().fetch_all(query)
    return schemas.TagGetList(tags=tags)


async def tag_delete(post_id: int, tag: str):
    query = Tag.delete().where(and_(Tag.c.post_id == post_id, Tag.c.tag == tag))
    await get_session().execute(query)
