from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base_model import MyBase


class Media(MyBase):
    """
    Класс orm модели Media.

    Attributes:
        tweet_id (int): id твита
        file_link (str): Путь до файла, который добавил пользователь
    """

    tweet_id: Mapped[int] = mapped_column(
        ForeignKey("tweets.id", ondelete="CASCADE"), nullable=True
    )
    file_link: Mapped[str] = mapped_column(VARCHAR(300), nullable=False)
