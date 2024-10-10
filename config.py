import os
from dotenv import load_dotenv
from fastapi.security import APIKeyHeader
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pathlib import Path


dotenv_path: str = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print('Переменные окружения загружены')

else:
    exit("Переменные окружения не загружены т.к отсутствует файл .env")


class StaticConfig(BaseModel):
    TEMPLATES_PATH: str = os.path.join(Path(__file__).parent, 'src', 'templates')
    STATIC_PATH: str = os.path.join(Path(__file__).parent, 'web', 'static')
    IMAGES_PATH: str = os.path.join(Path(__file__).parent, 'web', 'static', 'images')


class PostgresDbConfig(BaseModel):
    _db_name: str | None = os.getenv('DB_NAME')
    _dialect_db: str | None = os.getenv('DIALECT_DB')
    _driver_db: str | None = os.getenv('DRIVER_DB')
    _user_name_db: str | None = os.getenv('USER_NAME_DB')
    _user_pass_db: str | None = os.getenv('USER_PASS_DB')
    _host_db: str | None = os.getenv('HOST_DB')

    url_db_asyncpg: str = f"{_dialect_db}+{_driver_db}://{_user_name_db}:{_user_pass_db}@{_host_db}/{_db_name}"


class Settings(BaseSettings):
    """
    Base settings for program.
    """
    API_KEY_HEADER: APIKeyHeader = APIKeyHeader(name="api-key")
    APP_BASE_HOST: str = 'fastapi'
    APP_BASE_PORT: int = 8000
    APP_BASE_URL: str = f'http://{APP_BASE_HOST}:{APP_BASE_PORT}'
    BASE_DIR: Path = Path(__file__).parent
    api_v1_prefix: str = "/api/v1"
    db: PostgresDbConfig = PostgresDbConfig()
    static: StaticConfig = StaticConfig()


settings: Settings = Settings()
