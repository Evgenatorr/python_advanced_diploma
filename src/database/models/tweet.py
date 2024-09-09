from src.database.models.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import VARCHAR, ARRAY, INTEGER


class Tweet(Base):
    __tablename__ = "tweet"

    id: Mapped[int] = mapped_column(primary_key=True)
    tweet_data: Mapped[VARCHAR] = mapped_column(VARCHAR, nullable=False)
    tweet_media_ids: Mapped[ARRAY] = mapped_column(ARRAY(INTEGER))
    likes: Mapped[ARRAY] = mapped_column(ARRAY)

    author = relationship(argument='User', back_populates='tweets')

    def __repr__(self) -> str:
        return f"Tweet(id={self.id}, tweet_data={self.tweet_data}, tweet_media_ids={self.tweet_media_ids})"
