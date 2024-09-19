from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import VARCHAR, ARRAY, INTEGER, JSON
from src.database.models.base_model import MyBase


class Tweet(MyBase):
    content: Mapped[VARCHAR] = mapped_column(VARCHAR, nullable=False)
    attachments: Mapped[ARRAY] = mapped_column(ARRAY(String), nullable=True)
    author_id: Mapped[INTEGER] = mapped_column(INTEGER, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    likes = relationship(argument='Like', backref='tweet', lazy='subquery')
    author = relationship(argument='User', back_populates='tweets', lazy='selectin')

    # def __repr__(self) -> str:
    #     return (f"Tweet(id={self.id}, tweet_data={self.tweet_data}, "
    #             f"tweet_media_ids={self.tweet_media_ids}, likes={self.likes}, author={self.author}))")
