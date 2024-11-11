import os
from config import settings


def get_database_url() -> str:
    """
    Функция получения url базы данных
    :return: str
    """
    if os.environ.get('MODE') == "test":
        return settings.db_test.test_url_db_asyncpg

    return settings.db.url_db_asyncpg
