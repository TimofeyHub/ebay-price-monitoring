from typing import List, TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .sold_ad import SoldAd
from .base import Base
from .collection import collection_table

if TYPE_CHECKING:
    from .sold_ad import SoldAd


class ScaleModel(Base):
    __tablename__ = "scale_model"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    second_name: Mapped[str] = mapped_column(String(50))
    year: Mapped[int] = mapped_column(Integer())
    grand_prix: Mapped[str] = mapped_column(String(50))
    scale: Mapped[str] = mapped_column(String(20))
    brand: Mapped[str] = mapped_column(String(25))
    sold_ad: Mapped[List["SoldAd"]] = relationship(
        secondary=collection_table,
        back_populates="scale_model",
    )
