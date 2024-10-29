import uuid

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.database.async_session import get_async_session
from src.database.models.user_model import User
from src.schemas.user import UserCreate
from logs_conf.log_utils import logger

router = APIRouter(tags=["POST"])


@router.post("/api/users", status_code=status.HTTP_201_CREATED)
async def create_user(
        user_data: UserCreate = Depends(),
        session: AsyncSession = Depends(get_async_session),
) -> JSONResponse:
    """
    Роутер для создания нового пользователя
    :param user_data: данные пользователя
    :param session: асинхронная сессия базы данных
    :return: JSONResponse
    """
    user: User = await crud.user.user_crud.post(
        session=session, obj_in_data=user_data.model_dump()
    )
    random_api_key: str = str(uuid.uuid4())
    # random_api_key: str = 'test'
    api_data: dict[str, str | int] = {"api_key": random_api_key, "user_id": user.id}
    try:
        await crud.api_key.api_key_crud.post(session=session, obj_in_data=api_data)
    except IntegrityError as exc:
        logger.error('Такой api key уже существует', exc_info=exc)
        await session.rollback()
        return JSONResponse(
            content={"status": "false"},
            status_code=status.HTTP_409_CONFLICT
        )
    await session.refresh(user)
    logger.debug(f'Пользователь {user.name} создан, api key - {random_api_key}')
    return JSONResponse(
        content={"status": "true", "api_key": random_api_key, "user_id": user.id},
        status_code=status.HTTP_201_CREATED
    )
