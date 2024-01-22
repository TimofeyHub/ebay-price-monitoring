from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SoldAdBaseSchema(BaseModel):
    id_ebay: str
    raw_sold_date: str
    sold_date: datetime
    price: int
    ebay_link: str
    scale_model_id: int


class SoldAdSchema(SoldAdBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class SoldAdCreateSchema(SoldAdBaseSchema):
    pass


class SoldAdUpdateSchema(SoldAdBaseSchema):
    id_ebay: str | None = None
    raw_sold_date: str | None = None
    price: int | None = None
    ebay_link: str | None = None
