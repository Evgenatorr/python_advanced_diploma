import os

from fastapi import Depends, APIRouter
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src import crud
from src.database.async_session import get_async_session
from config import settings

router = APIRouter(tags=["POST"])
templates = Jinja2Templates(directory=os.path.join(settings.static.STATIC_PATH, 'admin'))


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
    users = await crud.user.user_crud.get_list(session=session)
    count_users = len(users)
    return templates.TemplateResponse(
        'get_all_users.html', {
            'request': request,
            'users': users,
            'count_users': count_users,
        }
    )
