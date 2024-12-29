import aiofiles
from fastapi import UploadFile

from logs_conf.log_utils import logger
from src.utils.create_unic_out_path import out_path


async def load_media(
        file: UploadFile,
) -> str | bool:
    """
    Функция загрузки изображения от пользователя на сервер
    :param file: изображение от пользователя
    :return: str
    """
    print(type(file))
    logger.debug('Загружаем изображение')
    if file.filename is None:
        return False
    unic_out_path: str = out_path(filename=file.filename)

    async with aiofiles.open(unic_out_path, "wb") as out_file:
        content: bytes = await file.read()
        await out_file.write(content)
    logger.info('Изображение успешно загружено')

    return unic_out_path
