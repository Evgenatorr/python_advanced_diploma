from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from src.crud.base_crud import BaseCrud
from src.database.models.user_model import User


class UserCrud(BaseCrud[User]):
    async def get_by_api_key(
        self, session: AsyncSession, api_key: str
    ) -> Optional[User]:
        """
        Функция получения объекта User по api_key с загрузкой связанных данных
        """
        query = await session.execute(
            select(self.model)
            .where(self.model.api_key == api_key)
            .options(
                selectinload(self.model.followers),
                selectinload(self.model.following)
            )
        )
        return query.scalar()

    async def get_with_lazy_load(
        self, session: AsyncSession, user_id: int
    ) -> Optional[User]:
        """
        Функция получения объекта User с загрузкой связанных данных
        """
        query = await session.execute(
            select(self.model)
            .where(self.model.id == user_id)
            .options(
                selectinload(self.model.followers),
                selectinload(self.model.following)
            )
        )
        return query.scalar()


user_crud = UserCrud(User)
