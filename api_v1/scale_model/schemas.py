from typing import Annotated

from pydantic import BaseModel, ConfigDict
from fastapi import Form


class ScaleModelBaseSchema(BaseModel):
    keywords: str
    year: int
    scale: str
    brand: str
    search_url_created_by_user: str | None = None


class ScaleModelCreateSchema(ScaleModelBaseSchema):
    keywords: Annotated[str, Form()]
    year: Annotated[int, Form()]
    scale: Annotated[str, Form()]
    brand: Annotated[str, Form()]
    search_url_created_by_user: Annotated[str | None, Form()] = None


class ScaleModelSchema(ScaleModelBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ScaleModelUpdateSchema(ScaleModelBaseSchema):
    keywords: str | None = None
    year: int | None = None
    scale: str | None = None
    brand: str | None = None
