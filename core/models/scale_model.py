from typing import List, TYPE_CHECKING, Optional

from sqlalchemy import String, Integer, ForeignKey
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
    keywords: Mapped[str] = mapped_column(String(255))
    year: Mapped[int] = mapped_column(Integer())
    scale: Mapped[str] = mapped_column(String(20))
    brand: Mapped[str] = mapped_column(String(25))
    search_url_created_by_user: Mapped[str] = mapped_column(String(), nullable=True)
    sold_ads: Mapped[List["SoldAd"]] = relationship(
        secondary=scale_model_and_ad_association,
        back_populates="scale_model",
    )
    collections: Mapped[List["Collection"]] = relationship(
        secondary=collection_and_scale_model_association,
        back_populates="scale_models",
    )
    # wishlists: Mapped[List["Wishlist"]] = relationship(
    #     secondary=wishlist_and_scale_model_association,
    #     back_populates="scale_models",
    # )
