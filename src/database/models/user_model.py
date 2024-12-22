from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from src.database.models.base_model import MyBase
from config import settings

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
        name (str): Имя пользователя
        api_key (bytes): Зашифрованный ключ пользователя
        tweets (Mapped[list[Tweet]]): Связь с orm моделью Tweet
        followers (Mapped[list[User]]): Самоссылающиеся отношения.
            Список подписчиков у пользователя
        following (Mapped[list[User]]): Самоссылающиеся отношения.
            Список подписок у пользователя
    """

    name: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    api_key: Mapped[bytes] = mapped_column(EncryptedType(
        VARCHAR, key=settings.ENCRYPTED_SECRET_KEY, engine=AesEngine
    ), nullable=False, unique=True, index=True)

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
