from src.database.models.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import VARCHAR, ARRAY


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[VARCHAR] = mapped_column(VARCHAR(50), nullable=False)
    followers: Mapped[ARRAY] = mapped_column(ARRAY, nullable=False)
    following: Mapped[ARRAY] = mapped_column(ARRAY, nullable=False)

    tweets = relationship(argument='Tweet', back_populates='author')

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name})"
