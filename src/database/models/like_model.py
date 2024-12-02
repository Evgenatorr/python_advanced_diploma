from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base_model import MyBase


class Like(MyBase):
    """
    Класс orm модели Like.

    Attributes:
        name (str): Имя пользователя
        user_id (int): id пользователя
        tweet_id (int): id твита
    """

    name: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    tweet_id: Mapped[int] = mapped_column(
        ForeignKey("tweets.id", ondelete="CASCADE"), nullable=False
    )
