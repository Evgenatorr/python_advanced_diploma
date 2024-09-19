from typing import Annotated
from fastapi import APIRouter, Depends, status, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.secure_user import get_user
from src.crud.tweet import tweet_crud
from src.database.session_manager import get_session
from src import schemas

router = APIRouter(tags=['POST'])


@router.post(
    "/api/medias", status_code=status.HTTP_201_CREATED
)
async def load_media(
        file: UploadFile, session: AsyncSession = Depends(get_session),
        user: schemas.user.UserResponse = Depends(get_user)
) -> JSONResponse:
    print(file)

    return JSONResponse(
        content={
            "result": "true",
            "media_id": 1,
        },
        status_code=status.HTTP_201_CREATED,
    )