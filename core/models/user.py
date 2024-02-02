from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .collection import Collection


# class User(Base):
#     __tablename__ = "user"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     username: Mapped[str] = mapped_column(String(20), unique=True)
#     about: Mapped[str] = mapped_column(String(255))
#     collection: Mapped["Collection"] = relationship(back_populates="user")
