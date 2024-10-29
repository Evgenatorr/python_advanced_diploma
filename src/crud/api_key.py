from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.api_key_model import ApiKey
from src.crud.base_crud import BaseCrud


class ApiKeyCrud(BaseCrud[ApiKey]):
    async def get_by_apikey(self, session: AsyncSession, api_key: str) -> Optional[ApiKey]:
        """
        Функция получения ApiKey объекта по столбцу api_key из базы данных
        """
        query = await session.execute(
            select(self.model).where(self.model.api_key == api_key)
        )
        return query.scalar()


api_key_crud = ApiKeyCrud(ApiKey)
