import os

from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from config import settings
from logs_conf.log_utils import logger
from src.crud import user_crud
from src.database.async_session import get_async_session

router = APIRouter(tags=["POST"])
templates = Jinja2Templates(
    directory=os.path.join(settings.static.STATIC_PATH, 'admin')
)


@router.post("/api/users", description='Роутер для вывода списка пользователей')
async def get_list_users(
        request: Request,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Роутер для вывода списка пользователей
    :param request: Request
    :param session: асинхронная сессия базы данных
    :return: JSONResponse
    """
    logger.debug(
        'Выводим таблицу с пользователями'
    )
    users = await user_crud.get_list(session=session)
    count_users = len(users)
    return templates.TemplateResponse(
        'get_all_users.html', {
            'request': request,
            'users': users,
            'count_users': count_users,
        }
    )
