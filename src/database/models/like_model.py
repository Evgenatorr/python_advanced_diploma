from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER
from src.database.models.base_model import MyBase


class Like(MyBase):
    name: Mapped[VARCHAR] = mapped_column(VARCHAR, nullable=False)
    user_id: Mapped[INTEGER] = mapped_column(INTEGER, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    tweet_id: Mapped[INTEGER] = mapped_column(INTEGER, ForeignKey('tweet.id', ondelete='CASCADE'), nullable=False)
    # tweet = relationship(argument='Tweet', back_populates='likes')
