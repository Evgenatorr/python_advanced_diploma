import os
from random import randint
from config import settings


def out_path(filename: str) -> str:
    random_num: str = str(randint(1, 999))
    path: str = os.path.join(settings.static.IMAGES_PATH, random_num + filename)
    while os.path.exists(path):
        random_num: str = str(randint(1, 999))
        path: str = os.path.join(settings.static.IMAGES_PATH, filename + random_num)

    return path
