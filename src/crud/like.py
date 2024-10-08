from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result

from src.database.models.like_model import Like


class LikeCrud:

    def __init__(self, model: Type[Like]) -> None:
        self.model: Type[Like] = model

    async def get(self, session: AsyncSession, like_id: int) -> Type[Like]:
        query: Type[Like] = await session.get(self.model, like_id)
        return query

    async def get_by_user_id_and_tweet_id(self, session: AsyncSession, tweet_id: int, user_id: int) -> Like:
        query: Result[tuple[Like]] = await session.execute(
            select(self.model)
            .where(
                self.model.tweet_id == tweet_id,
                self.model.user_id == user_id,
            )
        )
        return query.scalar()

    async def post(self, session: AsyncSession, like_data):
        like: Like = self.model(
            **like_data,
        )
        session.add(like)
        await session.commit()
        await session.refresh(like)
        return like

    async def delete(self, session: AsyncSession, like_id: int):
        db_obj: Type[Like] = await session.get(self.model, like_id)

        if not db_obj:
            return None

        await session.delete(db_obj)
        await session.commit()

        return db_obj


like_crud: LikeCrud = LikeCrud(Like)
