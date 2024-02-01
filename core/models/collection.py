from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .collection_and_scale_model import collection_and_scale_model_association

if TYPE_CHECKING:
    from .scale_model import ScaleModel


class Collection(Base):
    __tablename__ = "collection"
    id: Mapped[int] = mapped_column(primary_key=True)
    # user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    # user: Mapped["User"] = relationship(back_populates="collection")
    scale_models: Mapped[List["ScaleModel"]] = relationship(
        secondary=collection_and_scale_model_association,
        back_populates="collections",
    )
