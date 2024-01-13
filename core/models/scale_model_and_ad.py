from sqlalchemy import Table, Column, ForeignKey, Integer

from .base import Base

scale_model_and_ad_association = Table(
    "scale_model_and_ad_association",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("scale_model_id", ForeignKey("scale_model.id"), nullable=False),
    Column("sold_ad_id", ForeignKey("sold_ad.id"), nullable=False),
)
