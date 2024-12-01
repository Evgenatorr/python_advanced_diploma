from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            mapped_column)
from sqlalchemy.sql import func


class MyBase(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        # The table name is derived from the class name in lowercase
        return f'{cls.__name__.lower()}s'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now()
    )
    updated_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now()
    )
