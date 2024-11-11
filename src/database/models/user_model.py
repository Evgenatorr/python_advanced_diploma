from typing import List

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base_model import MyBase


followers = Table(
    "followers",
    MyBase.metadata,
    Column("follower_id", INTEGER, ForeignKey("user.id")),
    Column("followed_id", INTEGER, ForeignKey("user.id"))
)


class User(MyBase):
    name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)

    tweets = relationship(argument="Tweet", back_populates="author", lazy="selectin")
    # api_key = relationship(argument="ApiKey", back_populates="user", lazy="selectin")
    api_key: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    followers = relationship(
        "User",
        secondary=followers,
        primaryjoin="User.id == followers.c.followed_id",
        secondaryjoin="User.id == followers.c.follower_id",
        backref="following",
        lazy='selectin'
    )
