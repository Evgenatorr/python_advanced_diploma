import aiofiles
from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, schemas
from src.auth.secure_user import get_user_by_secure_key
from src.database.async_session import get_async_session
from src.database.models.media_model import Media
from src.utils.create_unic_out_path import out_path
from logs_conf.log_utils import logger

router = APIRouter(tags=["POST"])


async def load_media(
    file: UploadFile = File(...),
) -> str:
    """
    Функция загрузки изображения от пользователя на сервер
    :param file: изображение от пользователя
    :return: str
    """

    unic_out_path: str = out_path(filename=file.filename)
    async with aiofiles.open(unic_out_path, "wb") as out_file:
        content: bytes = await file.read()
        await out_file.write(content)
    logger.debug('Изображение успешно загружено')
    return unic_out_path


@router.post("/api/medias", status_code=status.HTTP_201_CREATED)
async def add_media(
    path: str = Depends(load_media),
    session: AsyncSession = Depends(get_async_session),
    current_user: schemas.user.UserResponse = Depends(get_user_by_secure_key),
) -> JSONResponse:
    """
    Роутер для добавления нового изображения
    :param path: путь изображения от пользователя
    :param session: асинхронная сессия базы данных
    :param current_user: пользователь прошедший аутентификацию
    :return: JSONResponse
    """

    file_name: str = path.split("/")[-1]
    path_nginx_image: str = f"/images/{file_name}"
    media: Media = await crud.media.media_crud.post(
        session=session, media_path=path_nginx_image
    )
    logger.debug('Изображение успешно добавлено в базу данных')
    return JSONResponse(
        content={
            "result": "true",
            "media_id": media.id,
        },
        status_code=status.HTTP_201_CREATED,
    )
