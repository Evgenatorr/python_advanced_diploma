from config import settings


def get_database_url() -> str:
    """
    Функция получения url базы данных
    :return: str
    """
    print(settings.START)
    if settings.START == "test":
        return settings.db_test.test_url_db_pgsync

    return settings.db.url_db_asyncpg
