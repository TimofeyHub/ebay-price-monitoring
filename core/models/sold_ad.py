from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class SoldAd(Base):
    __tablename__ = "sold_ad"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_ebay: Mapped[str] = mapped_column(unique=True)
    sold_date: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer())
    ebay_link: Mapped[str] = mapped_column(Text())
    id_model: Mapped[int] = mapped_column(ForeignKey("scale_model.id"))
