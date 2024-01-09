from sqlalchemy import Table, Column, ForeignKey, Integer

from .base import Base

collection_table = Table(
    "collection",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("scale_model_id", ForeignKey("scale_model.id"), nullable=False),
    Column("sold_ad_id", ForeignKey("sold_ad.id"), nullable=False),
)
