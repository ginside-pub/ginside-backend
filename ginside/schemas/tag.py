from pydantic import BaseModel


class Tag(BaseModel):
    post_id: int
    tag: str


class TagGet(Tag):
    pass


class TagGetList(BaseModel):
    tags: list[TagGet]
