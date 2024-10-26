from typing import Sequence, Type

from fastapi.encoders import jsonable_encoder
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models.user_model import User
from src.schemas.user import UserUpdateRequest


class UserCrud:

    def __init__(self, model: Type[User]):
        self.model: Type[User] = model

    async def get(self, session: AsyncSession, user_id: int) -> User | None:
        """
        Функция получения объекта User из таблицы по первичному ключу
        с загрузкой связанных данных
        :param session: асинхронная сессия базы данных
        :param user_id: первичный ключ таблицы
        :return: User | None
        """

        # query: User | None = await session.get(self.model, user_id)
        # return query
        query: Result[tuple[User]] = await session.execute(
            select(self.model).where(
                self.model.id == user_id,
            ).options(
                selectinload(self.model.followers), selectinload(self.model.following)
            )
        )
        return query.scalar()

    async def get_list(self, session: AsyncSession) -> Sequence[User]:
        """
        Функция получения списка объектов User из таблицы
        :param session: асинхронная сессия базы данных
        :return: Sequence[User]
        """

        query: Result[tuple[User]] = await session.execute(select(self.model))
        return query.scalars().all()

    async def post(self, session: AsyncSession, user_data) -> User:
        """
        Функция создания новой записи в таблице user
        :param session: асинхронная сессия базы данных
        :param user_data: данные для добавления записи в таблицу
        :return: User
        """

        user: User = self.model(**user_data)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def delete(self, session: AsyncSession, user_id: int) -> User | None:
        """
        Функция удаления записи из таблицы user по первичному ключу
        :param session: асинхронная сессия базы данных
        :param user_id: первичный ключ таблицы
        :return: User | None
        """

        db_obj: User | None = await self.get(session=session, user_id=user_id)

        if not db_obj:
            return None

        await session.delete(db_obj)
        await session.commit()

        return db_obj

    @staticmethod
    async def update(
            session: AsyncSession, current_user_data: User,
            new_user_data: UserUpdateRequest
    ) -> User:
        """
        Функция обновления записи в таблице user
        :param session: асинхронная сессия базы данных
        :param current_user_data: старые данные из таблицы
        :param new_user_data: новые данные из таблицы
        :return: User
        """

        user_data = jsonable_encoder(current_user_data)
        update_data = new_user_data.model_dump(exclude_unset=True)
        for field in user_data:
            if field in update_data:
                setattr(
                    current_user_data, field, update_data[field]
                )  # current_user_data.field = update_data[field]

        session.add(current_user_data)
        await session.commit()
        await session.refresh(current_user_data)
        return current_user_data


user_crud: UserCrud = UserCrud(User)
