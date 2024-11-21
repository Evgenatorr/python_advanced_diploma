from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base_model import MyBase


class Media(MyBase):
    # filename: Mapped[VARCHAR] = mapped_column(VARCHAR, nullable=False)
    tweet_id: Mapped[int] = mapped_column(
        INTEGER, ForeignKey("tweets.id", ondelete="CASCADE"), nullable=True
    )
    file_link: Mapped[str] = mapped_column(VARCHAR, nullable=False)
