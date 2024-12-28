from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from logs_conf.log_utils import logger
from src.auth.secure_user import get_user_by_secure_key
from src.crud import media_crud
from src.database.async_session import get_async_session
from src.database.models.media_model import Media
from src.routes.dependencies.load_media import load_media
from src.schemas import CreateMedia, UserResponse, ResponseMedia

router = APIRouter(tags=["POST"])


@router.post("/api/medias", status_code=status.HTTP_201_CREATED,
             response_model=ResponseMedia)
async def add_media(
    path: str = Depends(load_media),
    session: AsyncSession = Depends(get_async_session),
    current_user: UserResponse = Depends(get_user_by_secure_key),
) -> JSONResponse:
    logger.debug('Добавляем изображение в базу данных')
    """
    Роутер для добавления нового изображения
    :param path: путь изображения от пользователя
    :param session: асинхронная сессия базы данных
    :param current_user: пользователь прошедший аутентификацию
    :return: JSONResponse
    """
    if path:
        file_name: str = path.split("/")[-1]
        image_data: CreateMedia = CreateMedia(
            file_name=file_name
        )
        new_media: Media = await media_crud.post(
            session=session, obj_in_data=image_data.model_dump()
        )
        logger.info('Изображение успешно добавлено в базу данных')
        return JSONResponse(
            content={
                "result": "true",
                "media_id": new_media.id,
            },
            status_code=status.HTTP_201_CREATED,
        )

    return JSONResponse(
        content={
            "result": "false",
        },
        status_code=status.HTTP_400_BAD_REQUEST,
    )
