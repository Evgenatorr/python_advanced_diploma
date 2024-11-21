from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base_model import MyBase


class Like(MyBase):
    name: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    user_id: Mapped[int] = mapped_column(
        INTEGER, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    tweet_id: Mapped[int] = mapped_column(
        INTEGER, ForeignKey("tweets.id", ondelete="CASCADE"), nullable=False
    )
