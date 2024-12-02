from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base_model import MyBase


class Tweet(MyBase):
    """
    Класс orm модели Tweet.

    Attributes:
        content (str): Сообщение, что написал пользователь в твит
        attachments (list[str]): Список картинок, которые пользователь добавил в твит
        author_id (int): id автора твита
        media (Mapped[Media]): Связь с orm моделью Media
        likes (Mapped[list[Like]]): Связь с orm моделью Like
        author (Mapped[User]): Связь с orm моделью User
    """

    content: Mapped[str] = mapped_column(VARCHAR(300), nullable=False)
    attachments: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    media = relationship(
        argument="Media", backref="tweet", lazy="selectin", cascade="all, delete"
    )
    likes = relationship(
        argument="Like", backref="tweet", lazy="selectin", cascade="all, delete"
    )
    author = relationship(argument="User", back_populates="tweets", lazy="selectin")
