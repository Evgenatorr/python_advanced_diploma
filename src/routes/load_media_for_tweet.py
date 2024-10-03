import os
from pathlib import Path

from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.responses import JSONResponse
import aiofiles
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings
from src import crud
from src.auth.secure_user import get_user_by_secure_key
from src.database.session_manager import get_async_session
from src import schemas
from src.utils.create_unic_out_path import out_path

router = APIRouter(tags=['POST'])


async def load_media(
        file: UploadFile = File(...),
):
    unic_out_path = out_path(filename=file.filename)
    async with aiofiles.open(unic_out_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    return unic_out_path


@router.post(
    "/api/medias", status_code=status.HTTP_201_CREATED
)
async def add_media(
        path: str = Depends(load_media), session: AsyncSession = Depends(get_async_session),
        current_user: schemas.user.UserResponse = Depends(get_user_by_secure_key)
) -> JSONResponse:
    file_name = path.split('/')[-1]
    path_nginx_image = f'/images/{file_name}'
    media = await crud.media.media_crud.post(session=session, media_path=path_nginx_image)

    return JSONResponse(
        content={
            "result": "true",
            "media_id": media.id,
        },
        status_code=status.HTTP_201_CREATED,
    )
