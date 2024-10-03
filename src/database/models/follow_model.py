from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER
from src.database.models.base_model import MyBase


# class Followers(MyBase):
#     follower_id = mapped_column(INTEGER, ForeignKey('user.id'))
#     followed_id = mapped_column(INTEGER, ForeignKey('user.id'))


#
# class Following(MyBase):
#     name: Mapped[VARCHAR] = mapped_column(VARCHAR(50), nullable=False)
#     user_id = mapped_column(INTEGER, ForeignKey('user.id'))
#
#
# class Followers(MyBase):
#     name: Mapped[VARCHAR] = mapped_column(VARCHAR(50), nullable=False)
#     user_id = mapped_column(INTEGER, ForeignKey('user.id'))
