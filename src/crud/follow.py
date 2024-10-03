# from typing import Type
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from src.database.models.follow_model import Followers
#
#
# class FollowCrud:
#
#     def __init__(self, model: Type[Followers]):
#         self.model = model
#
#     async def get(self, session: AsyncSession, follow_id: int):
#         query = await session.get(self.model, follow_id)
#         return query
#
#     async def post(self, session: AsyncSession, follow_data):
#         follow = self.model(
#             **follow_data,
#         )
#         session.add(follow)
#         await session.commit()
#         await session.refresh(follow)
#         return follow
#
#     async def delete(self, session: AsyncSession, follow_id: int):
#         db_obj = await session.get(self.model, follow_id)
#
#         if not db_obj:
#             return None
#
#         await session.delete(db_obj)
#         await session.commit()
#
#         return db_obj
#
#
# following_crud = FollowCrud(Followers)
