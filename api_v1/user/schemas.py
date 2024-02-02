from typing import Annotated

from fastapi import Form
from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    email: str
    password: str


class UserSchema(UserBaseSchema):
    id: int


class CreateUserSchema(UserBaseSchema):
    email: Annotated[str, Form()]
    password: Annotated[str, Form()]
