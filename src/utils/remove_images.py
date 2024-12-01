import os
from typing import List

from config import settings


async def del_images(medias: List[str]) -> None:
    for media in medias:
        if os.path.exists(settings.static.STATIC_PATH + media):
            os.remove(settings.static.STATIC_PATH + media)
