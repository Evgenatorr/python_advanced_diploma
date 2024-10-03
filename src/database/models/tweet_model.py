from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import VARCHAR, ARRAY, INTEGER, JSON
from src.database.models.base_model import MyBase


class Tweet(MyBase):
    content: Mapped[VARCHAR] = mapped_column(VARCHAR, nullable=False)
    attachments: Mapped[ARRAY] = mapped_column(ARRAY(String), nullable=True)
    author_id: Mapped[INTEGER] = mapped_column(
        INTEGER, ForeignKey('user.id', ondelete='CASCADE'), nullable=False
    )
    # media_id: Mapped[INTEGER] = mapped_column(
    #     INTEGER, ForeignKey('media.id'), nullable=True
    # )

    media = relationship(argument='Media', backref='tweet', lazy='selectin', cascade="all, delete")
    likes = relationship(argument='Like', backref='tweet', lazy='selectin', cascade="all, delete")
    author = relationship(argument='User', back_populates='tweets', lazy='selectin')

    # def __repr__(self) -> str:
    #     return (f"Tweet(id={self.id}, tweet_data={self.tweet_data}, "
    #             f"likes={self.likes}, author={self.author}))")
