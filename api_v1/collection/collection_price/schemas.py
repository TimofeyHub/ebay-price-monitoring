from pydantic import BaseModel, ConfigDict


class CollectionPriceBaseSchema(BaseModel):
    id_collection: int
    min_price: int
    max_price: int


class CollectionPriceSchema(CollectionPriceBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CollectionPriceCreateSchema(CollectionPriceBaseSchema):
    pass
