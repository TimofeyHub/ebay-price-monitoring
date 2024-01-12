from pydantic import BaseModel, ConfigDict


class ScaleModelBaseSchema(BaseModel):
    first_name: str
    second_name: str
    year: int
    grand_prix: str
    scale: str
    brand: str


class ScaleModelCreateSchema(ScaleModelBaseSchema):
    pass


class ScaleModelSchema(ScaleModelBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ScaleModelUpdateSchema(ScaleModelBaseSchema):
    first_name: str | None = None
    second_name: str | None = None
    year: int | None = None
    grand_prix: str | None = None
    scale: str | None = None
    brand: str | None = None
