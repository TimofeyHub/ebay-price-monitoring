from sqlalchemy import Column, ForeignKey, Table, Integer

from .base import Base

wishlist_and_scale_model_association = Table(
    "wishlist_and_scale_model",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("wishlist_id", ForeignKey("wishlist.id"), nullable=False),
    Column("scale_model_id", ForeignKey("scale_model.id"), nullable=False),
)
