from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base_model import MyBase

follow = Table(
    "followers",
    MyBase.metadata,
    Column("follower_id", INTEGER, ForeignKey("users.id")),
    Column("followed_id", INTEGER, ForeignKey("users.id"))
)


class User(MyBase):
    """
    Класс orm модели Tweet.

    Attributes:
        name (str): Сообщение, что написал пользователь в твит
        api_key (list[str]): Список картинок, которые пользователь добавил в твит
        tweets (Mapped[list[Tweet]]): Связь с orm моделью Tweet
        followers (Mapped[list[User]]): Самоссылающиеся отношения.
            Список подписчиков у пользователя
        following (Mapped[list[User]]): Самоссылающиеся отношения.
            Список подписок у пользователя
    """

    name: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    api_key: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)

    tweets = relationship(argument="Tweet", back_populates="author", lazy="selectin")
    followers = relationship(
        "User",
        secondary=follow,
        primaryjoin="User.id == followers.c.follower_id",
        secondaryjoin="User.id == followers.c.followed_id",
        back_populates="following",
    )
    following = relationship(
        "User",
        secondary=follow,
        primaryjoin="User.id == followers.c.followed_id",
        secondaryjoin="User.id == followers.c.follower_id",
        back_populates="followers",
    )
