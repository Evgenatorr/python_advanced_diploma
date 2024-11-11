import os

from fastapi import APIRouter, Depends, status, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.database.async_session import get_async_session
from src.database.models.user_model import User
from src.schemas.user import UserCreate
from config import settings
from logs_conf.log_utils import logger

router = APIRouter(tags=["POST"])
templates = Jinja2Templates(directory=os.path.join(settings.static.STATIC_PATH, 'admin'))


@router.post("/api/create_user", description='Роутер для создания нового пользователя',
             response_model=None)
async def create_user(
        name: str = Form(pattern=r'[a-zA-Zа-яА-Я]'),
        api_key: str = Form(...),
        session: AsyncSession = Depends(get_async_session),
) -> JSONResponse | RedirectResponse:
    """
    Роутер для создания нового пользователя
    :param api_key: api key пользователя
    :param name: имя пользователя
    :param session: асинхронная сессия базы данных
    :return: JSONResponse
    """

    user_data = UserCreate(
        name=name,
        api_key=api_key,
    )
    try:
        user: User = await crud.user.user_crud.post(
            session=session, obj_in_data=user_data.model_dump()
        )

    except IntegrityError as exc:
        logger.error('Такой api key уже существует', exc_info=exc)
        await session.rollback()
        return JSONResponse(
            content={
                "status": "false",
                "error_message": "Такой api key уже существует"
            },
            status_code=status.HTTP_409_CONFLICT
        )
    logger.debug(f'Пользователь {user.name} создан, api key - {user.api_key}')

    return RedirectResponse("/api/users")


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
