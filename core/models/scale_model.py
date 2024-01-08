from typing import List

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .sold_ad import SoldAd
from .base import Base


class ScaleModel(Base):
    __tablename__ = "scale_model"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    second_name: Mapped[str] = mapped_column(String(50))
    year: Mapped[int] = mapped_column(Integer())
    grand_prix: Mapped[str] = mapped_column(String(50))
    scale: Mapped[str] = mapped_column(String(20))
    brand: Mapped[str] = mapped_column(String(25))
    sold_ad: Mapped[List["SoldAd"]] = relationship()
