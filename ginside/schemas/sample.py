from datetime import datetime

from pydantic import BaseModel


class Sample(BaseModel):
    description: str | None


class SampleCreate(Sample):
    name: str


class SampleUpdate(Sample):
    pass


class SampleGet(SampleCreate):
    id: int
    created_at: datetime
    updated_at: datetime | None


class SampleGetList(BaseModel):
    samples: list[SampleGet]
