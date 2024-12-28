import os
from typing import List

from config import settings


async def del_images(medias: List[str]) -> None:
    for media in medias:
        path = os.path.join(settings.static.IMAGES_PATH, media)
        if os.path.exists(path):
            os.remove(path)
