from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER
from src.database.models.base_model import MyBase


class ApiKey(MyBase):
    api_key: Mapped[VARCHAR] = mapped_column(VARCHAR, nullable=False, unique=True)
    user_id: Mapped[INTEGER] = mapped_column(INTEGER, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    user = relationship(argument='User', back_populates='api_key', lazy='joined')

    # def __repr__(self) -> str:
    #     return f"ApiKey(id={self.id}, api_key={self.api_key}, user_id={self.user_id}, user={self.user})"
