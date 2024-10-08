from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result

from src.database.models.api_key_model import ApiKey


class ApiKeyCrud:

    def __init__(self, model: Type[ApiKey]):
        self.model: Type[ApiKey] = model

    async def get_by_apikey(self, session: AsyncSession, api_key: str) -> ApiKey:
        query: Result[tuple[ApiKey]] = await session.execute(select(self.model).where(self.model.api_key == api_key))
        return query.scalar()

    async def post(self, session: AsyncSession, api_key_data) -> ApiKey:
        api_key_model: ApiKey = self.model(**api_key_data)
        session.add(api_key_model)
        await session.commit()
        await session.refresh(api_key_model)
        return api_key_model


api_key_crud: ApiKeyCrud = ApiKeyCrud(ApiKey)
