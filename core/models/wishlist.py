from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .wishlist_and_scale_model import wishlist_and_scale_model_association

if TYPE_CHECKING:
    from .user import User
    from .scale_model import ScaleModel


class Wishlist(Base):
    __tablename__ = "wishlist"
    id: Mapped[int] = mapped_column(primary_key=True)
    # user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    # user: Mapped["User"] = relationship(back_populates="wishlist")
    # scale_models: Mapped[List["ScaleModel"]] = relationship(
    #     secondary=wishlist_and_scale_model_association,
    #     back_populates="wishlists",
    # )
