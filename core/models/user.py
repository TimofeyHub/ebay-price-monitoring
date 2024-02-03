from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .collection import Collection
    from .cookie import CookieInfo


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    collection: Mapped["Collection"] = relationship(back_populates="user")
    cookies: Mapped[List["CookieInfo"]] = relationship(back_populates="user")
