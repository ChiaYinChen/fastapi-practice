"""Settings."""
import logging.config
from os.path import abspath, dirname, join
from typing import Any, Dict, Optional

from pydantic import BaseSettings, validator
from sqlalchemy.engine.url import URL


class Settings(BaseSettings):

    SECRET_KEY: str = "TEST_SECRET_DO_NOT_USE_IN_PROD"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = 'pgsql_db'
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        postgres_db = {
            'drivername': 'postgresql',
            'username': values.get("POSTGRES_USER"),
            'password': values.get("POSTGRES_PASSWORD"),
            'host': values.get("POSTGRES_HOST"),
            'port': values.get("POSTGRES_PORT"),
            'database': values.get("POSTGRES_DB")
        }
        return str(URL.create(**postgres_db))

    TEST_USER_EMAIL: str = "test@example.com"
    TEST_USER_USERNAME: str = "testuser"
    TEST_USER_PASSWORD: str = "testuserpass"
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_SUPERUSER_EMAIL: str = "testsuper@example.com"

    class Config:
        env_file = './env/.prod.env'
        case_sensitive = True


settings = Settings()

# logging setting
PROJ_ROOT = dirname(dirname(dirname(abspath(__file__))))
LOG_FILE_PATH = join(PROJ_ROOT, 'app', 'logging.conf')
logging.config.fileConfig(LOG_FILE_PATH)
