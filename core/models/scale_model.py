from typing import List, TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .collection_and_scale_model import collection_and_scale_model_association
from .scale_model_and_ad import scale_model_and_ad_association
from .wishlist_and_scale_model import wishlist_and_scale_model_association

if TYPE_CHECKING:
    from .sold_ad import SoldAd
    from .collection import Collection
    from .wishlist import Wishlist


class ScaleModel(Base):
    __tablename__ = "scale_model"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(
        String(50),
        nullable=True,
        default="",
        server_default="",
    )
    second_name: Mapped[str] = mapped_column(String(50))
    year: Mapped[int] = mapped_column(Integer())
    grand_prix: Mapped[str] = mapped_column(String(50))
    scale: Mapped[str] = mapped_column(String(20))
    brand: Mapped[str] = mapped_column(String(25))
    sold_ads: Mapped[List["SoldAd"]] = relationship(
        secondary=scale_model_and_ad_association,
        back_populates="scale_model",
    )
    collections: Mapped[List["Collection"]] = relationship(
        secondary=collection_and_scale_model_association,
        back_populates="scale_models",
    )
    wishlists: Mapped[List["Wishlist"]] = relationship(
        secondary=wishlist_and_scale_model_association,
        back_populates="scale_models",
    )
