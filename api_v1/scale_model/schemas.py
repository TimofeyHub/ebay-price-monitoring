from pydantic import BaseModel, ConfigDict


class ScaleModelBaseSchema(BaseModel):
    keywords: str
    year: int
    scale: str
    brand: str


class ScaleModelCreateSchema(ScaleModelBaseSchema):
    pass


class ScaleModelSchema(ScaleModelBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ScaleModelUpdateSchema(ScaleModelBaseSchema):
    keywords: str | None = None
    year: int | None = None
    scale: str | None = None
    brand: str | None = None
