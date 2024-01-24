from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from .base import Base
from .scale_model_and_ad import scale_model_and_ad_association

if TYPE_CHECKING:
    from .scale_model import ScaleModel

NOT_INCLUDE_IN_CALCULATION_STATUS = 0


class SoldAd(Base):
    __tablename__ = "sold_ad"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_ebay: Mapped[str] = mapped_column(nullable=False)
    raw_sold_date: Mapped[str] = mapped_column(String(100))
    sold_date: Mapped[DateTime] = mapped_column(DateTime())
    price: Mapped[int] = mapped_column(Integer())
    ebay_link: Mapped[str] = mapped_column(Text())
    include_in_calculation: Mapped[bool] = mapped_column(
        Boolean(),
        server_default=expression.true(),
        default=True,
    )
    scale_model_id: Mapped[int] = mapped_column(ForeignKey("scale_model.id"))
    scale_model: Mapped["ScaleModel"] = relationship(
        secondary=scale_model_and_ad_association,
        back_populates="sold_ads",
    )
