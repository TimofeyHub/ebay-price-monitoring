from pydantic import BaseModel


class CookieInfoBaseSchema(BaseModel):
    session_id: str
    user_id: int


class CookieInfoSchema(CookieInfoBaseSchema):
    id: int


class CreateCookieInfoSchema(CookieInfoBaseSchema):
    pass
