from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER
from src.database.models.base_model import MyBase


class Media(MyBase):
    # filename: Mapped[VARCHAR] = mapped_column(VARCHAR, nullable=False)
    tweet_id: Mapped[INTEGER] = mapped_column(INTEGER, ForeignKey('tweet.id', ondelete='CASCADE'), nullable=True)
    file_link: Mapped[VARCHAR] = mapped_column(VARCHAR, nullable=False)
    # tweet = relationship(argument='Tweet', backref='medias', lazy='subquery', cascade="all, delete")
