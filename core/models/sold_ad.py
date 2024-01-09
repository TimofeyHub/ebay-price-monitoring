from typing import List, TYPE_CHECKING

from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .collection import collection_table

if TYPE_CHECKING:
    from .scale_model import ScaleModel


class SoldAd(Base):
    __tablename__ = "sold_ad"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_ebay: Mapped[str] = mapped_column(unique=True)
    sold_date: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer())
    ebay_link: Mapped[str] = mapped_column(Text())
    sold_ad: Mapped[List["ScaleModel"]] = relationship(
        secondary=collection_table,
        back_populates="sold_ad",
    )
