from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi.encoders import jsonable_encoder

from src.database.models.tweet_model import Tweet
from src.schemas.tweet import TweetUpdateRequest


class TweetCrud:

    def __init__(self, model: Type[Tweet]):
        self.model = model

    async def get(self, session: AsyncSession, tweet_id: int):
        query = await session.get(self.model, tweet_id)
        return query

    async def get_list_by_user_id(self, session: AsyncSession, user_id: int):
        query = await session.execute(select(self.model).where(self.model.author_id == user_id))
        return query.scalars().all()

    async def get_list(self, session: AsyncSession):
        query = await session.execute(select(self.model))
        return query.scalars().all()

    async def post(self, session: AsyncSession, tweet_data, author_id: int):
        tweet = self.model(
            **tweet_data
        )
        tweet.author_id = author_id
        session.add(tweet)
        await session.commit()
        await session.refresh(tweet)
        return tweet

    async def delete(self, session: AsyncSession, tweet_id: int):
        db_obj = await session.get(self.model, tweet_id)

        if not db_obj:
            return None

        await session.delete(db_obj)
        await session.commit()

        return db_obj

    async def update(self, session: AsyncSession, current_tweet_data: Tweet, new_tweet_data: TweetUpdateRequest):
        tweet_data = jsonable_encoder(current_tweet_data)
        update_data = new_tweet_data.model_dump(exclude_unset=True)

        for field in tweet_data:
            if field in update_data:
                setattr(current_tweet_data, field, update_data[field])  # current_tweet_data.field = update_data[field]

        session.add(current_tweet_data)
        await session.commit()
        await session.refresh(current_tweet_data)
        return current_tweet_data


tweet_crud = TweetCrud(Tweet)
