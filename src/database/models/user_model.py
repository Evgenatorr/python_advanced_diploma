from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base_model import MyBase


user_following = Table(
    "user_following",
    MyBase.metadata,
    Column("followers_id", INTEGER, ForeignKey("user.id"), primary_key=True),
    Column("following_id", INTEGER, ForeignKey("user.id"), primary_key=True),
)


class User(MyBase):
    name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)

    tweets = relationship(argument="Tweet", back_populates="author", lazy="selectin")
    api_key = relationship(argument="ApiKey", back_populates="user", lazy="selectin")
    # following: Mapped[ARRAY] = mapped_column(ARRAY(JSON), nullable=True)
    # followers: Mapped[ARRAY] = mapped_column(ARRAY(JSON), nullable=True)
    # following = relationship(
    #     'User', lambda: user_following,
    #     primaryjoin=lambda: User.id == user_following.c.user_id,
    #     secondaryjoin=lambda: User.id == user_following.c.following_id,
    #     backref=backref('followers', lazy='dynamic'),
    #     lazy='dynamic'
    # )
    following = relationship(
        "User",
        secondary=user_following,
        primaryjoin="User.id == user_following.c.followers_id",
        secondaryjoin="User.id == user_following.c.following_id",
        back_populates="followers",
        lazy="dynamic",
    )
    followers = relationship(
        "User",
        secondary=user_following,
        primaryjoin="User.id == user_following.c.following_id",
        secondaryjoin="User.id == user_following.c.followers_id",
        back_populates="following",
        lazy="dynamic",
    )


# following: Mapped[List['User']] = relationship(
#     'User',
#     secondary='user_following',
#     primaryjoin='User.id == user_following.c.user_id',
#     secondaryjoin='User.id == user_following.c.following_id',
#     back_populates='followers',
#     lazy='dynamic',
# )
# followers: Mapped[List['User']] = relationship(
#     'User',
#     secondary='user_following',
#     primaryjoin='User.id == user_following.c.following_id',
#     secondaryjoin='User.id == user_following.c.user_id',
#     back_populates='following',
#     lazy='dynamic',
# )
