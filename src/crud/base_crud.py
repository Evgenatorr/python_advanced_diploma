from typing import Type, TypeVar, Generic, Sequence, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.encoders import jsonable_encoder

ModelType = TypeVar("ModelType")


class BaseCrud(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def get(self, session: AsyncSession, id: int) -> Optional[ModelType]:
        """
        Получение объекта по первичному ключу
        """
        return await session.get(self.model, id)

    async def get_list(self, session: AsyncSession) -> Sequence[ModelType]:
        """
        Получение списка объектов
        """
        query = await session.execute(select(self.model))
        return query.scalars().all()

    async def post(self, session: AsyncSession, obj_in_data: dict) -> ModelType:
        """
        Создание нового объекта
        """
        obj_in = self.model(**obj_in_data)
        session.add(obj_in)
        await session.commit()
        await session.refresh(obj_in)
        return obj_in

    async def update(self, session: AsyncSession, db_obj: ModelType, obj_in_data: dict) -> ModelType:
        """
        Обновление существующего объекта
        """
        obj_data = jsonable_encoder(db_obj)
        updated_fields = {field: obj_in_data[field] for field in obj_data if field in obj_in_data}

        for field, value in updated_fields.items():
            setattr(db_obj, field, value)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, id: int) -> Optional[ModelType]:
        """
        Удаление объекта по первичному ключу
        """
        obj = await self.get(session, id)
        if obj:
            await session.delete(obj)
            await session.commit()
        return obj
