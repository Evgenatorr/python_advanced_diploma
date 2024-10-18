from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY, INTEGER, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base_model import MyBase


class Tweet(MyBase):
    content: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    attachments: Mapped[ARRAY] = mapped_column(ARRAY(String), nullable=True)
    author_id: Mapped[int] = mapped_column(
        INTEGER, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    media = relationship(
        argument="Media", backref="tweet", lazy="selectin", cascade="all, delete"
    )
    likes = relationship(
        argument="Like", backref="tweet", lazy="selectin", cascade="all, delete"
    )
    author = relationship(argument="User", back_populates="tweets", lazy="selectin")
