from sqlalchemy import MetaData
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            mapped_column)
from sqlalchemy.sql import func

convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()]
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}


class MyBase(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        # The table name is derived from the class name in lowercase
        return cls.__name__.lower()

    metadata = MetaData(naming_convention=convention)  # type: ignore

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, index=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now()
    )
    updated_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now()
    )
