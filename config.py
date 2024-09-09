import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pathlib import Path


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print('Переменные окружения загружены')

else:
    exit("Переменные окружения не загружены т.к отсутствует файл .env")


class PostgresDbConfig(BaseModel):
    _db_name: str = os.getenv('DB_NAME')
    _dialect_db: str = os.getenv('DIALECT_DB')
    _driver_db: str = os.getenv('DRIVER_DB')
    _user_name_db: str = os.getenv('USER_NAME_DB')
    _user_pass_db: str = os.getenv('USER_PASS_DB')
    _host_db: str = os.getenv('HOST_DB')

    url_db_asyncpg: str = f"{_dialect_db}+{_driver_db}://{_user_name_db}:{_user_pass_db}@{_host_db}/{_db_name}"


class Settings(BaseSettings):
    """
    Base settings for program.
    """

    APP_BASE_HOST: str = 'fastapi'
    APP_BASE_PORT: str = '8000'
    APP_BASE_URL: str = f'http://{APP_BASE_HOST}:{APP_BASE_PORT}'
    BASE_DIR = Path(__file__).parent
    api_v1_prefix: str = "/api/v1"
    db: PostgresDbConfig = PostgresDbConfig()


settings = Settings()
