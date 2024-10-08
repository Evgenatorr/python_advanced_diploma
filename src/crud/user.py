from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, ScalarResult, Result
from sqlalchemy.orm import AppenderQuery
from fastapi.encoders import jsonable_encoder

from src.database.models.user_model import User
from src.schemas.user import UserUpdateRequest, UserPatchRequest


class UserCrud:

    def __init__(self, model: Type[User]):
        self.model: Type[User] = model

    async def get(self, session: AsyncSession, user_id: int) -> Type[User] | None:
        query: Type[User] | None = await session.get(self.model, user_id)
        return query

    @staticmethod
    async def get_list_followers_by_user(session: AsyncSession, user: User) -> ScalarResult:
        query: AppenderQuery = user.followers
        followers: ScalarResult = await session.scalars(query)
        return followers

    @staticmethod
    async def get_list_following_by_user(session: AsyncSession, user: User) -> ScalarResult:
        query: AppenderQuery = user.following
        following: ScalarResult = await session.scalars(query)
        return following

    async def get_list(self, session: AsyncSession):
        query: Result[tuple[User]] = await session.execute(select(self.model))
        return query.scalars().all()

    async def post(self, session: AsyncSession, user_data):
        user: User = self.model(**user_data)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def delete(self, session: AsyncSession, user_id: int):
        db_obj = self.get(session=session, user_id=user_id)

        if not db_obj:
            return None

        await session.delete(db_obj)
        await session.commit()

        return db_obj

    async def update(self, session: AsyncSession, current_user_data: User, new_user_data: UserUpdateRequest):
        user_data = jsonable_encoder(current_user_data)
        update_data = new_user_data.model_dump(exclude_unset=True)
        for field in user_data:
            if field in update_data:
                setattr(current_user_data, field, update_data[field])  # current_user_data.field = update_data[field]

        session.add(current_user_data)
        await session.commit()
        await session.refresh(current_user_data)
        return current_user_data

    async def patch(self, session: AsyncSession, user_id: int, new_user_data: UserPatchRequest):
        db_obj = await self.get(session=session, user_id=user_id)
        if not db_obj:
            return None

        update_data = new_user_data.model_dump(exclude_unset=True)
        query = (
            update(self.model)
            .where(self.model.id == user_id)
            .values(**update_data)
        )
        await session.execute(query)
        return await self.get(session=session, user_id=user_id)


user_crud = UserCrud(User)
