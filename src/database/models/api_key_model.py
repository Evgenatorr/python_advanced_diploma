from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base_model import MyBase


class ApiKey(MyBase):
    api_key: Mapped[str] = mapped_column(VARCHAR, nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(
        INTEGER, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship(argument="User", back_populates="api_key", lazy="joined")
