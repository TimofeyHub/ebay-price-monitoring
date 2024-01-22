from datetime import datetime

from sqlalchemy import ForeignKey, Integer, DateTime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

current_time = datetime.now()


class CollectionPrice(Base):
    __tablename__ = "collection_price"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_collection: Mapped[int] = mapped_column(ForeignKey("collection.id"))
    min_price: Mapped[int] = mapped_column(Integer())
    max_price: Mapped[int] = mapped_column(Integer())
    update_date: Mapped[datetime] = mapped_column(
        DateTime(),
        server_default=func.now(),
        default=datetime.utcnow,
    )
