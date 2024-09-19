from sqlalchemy import INTEGER

from src.database.models.base_model import MyBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import VARCHAR, ARRAY, JSON, INTEGER


class User(MyBase):
    name: Mapped[VARCHAR] = mapped_column(VARCHAR(50), nullable=False)
    followers: Mapped[ARRAY] = mapped_column(ARRAY(JSON), nullable=True)
    following: Mapped[ARRAY] = mapped_column(ARRAY(JSON), nullable=True)

    tweets = relationship(argument='Tweet', back_populates='author', lazy='joined')
    api_key = relationship(argument='ApiKey', back_populates='user', lazy='joined')

    # def __repr__(self) -> str:
    #     return (f"User(id={self.id}, name={self.name}, api_key={self.api_key}, "
    #             f"followers={self.followers}, following={self.following}, tweets={self.tweets})")
