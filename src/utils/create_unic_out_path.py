import os
import uuid

from config import settings


def out_path(filename: str) -> str:
    """
    Функция генерации пути для хранения картинки от пользователя
    :param filename: название файла с изображением
    :return: str
    """

    random_num: str = uuid.uuid4().hex
    if os.environ.get('MODE') == "test":
        return os.path.join(settings.TEST_IMAGES_DIR, random_num + filename)
    else:
        return os.path.join(settings.static.IMAGES_PATH, random_num + filename)
