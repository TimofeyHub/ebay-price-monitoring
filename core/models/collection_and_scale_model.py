from sqlalchemy import Column, ForeignKey, Table, Integer

from .base import Base

collection_and_scale_model_association = Table(
    "collection_and_scale_model",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("collection_id", ForeignKey("collection.id"), nullable=False),
    Column("scale_model_id", ForeignKey("scale_model.id"), nullable=False),
)
