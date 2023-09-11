from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_SCHEME: str = "postgresql+asyncpg"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "brightlab-db"

    SECRET_KEY: str = "TrE55giQ8nLAWvFYpsLxe/zkZNHcQP9fIwe4ys+zD3A="
    ALGORITHM: str = "HS256"
    REFRESH_TOKEN_COOKIE_NAME: str = "app-refresh-token"
    REFRESH_TOKEN_EXP_DAYS: int = 14
    ACCESS_TOKEN_EXP_MINS: int = 10

    @property
    def database_url(self):
        dsn = PostgresDsn.build(
            scheme=self.DB_SCHEME,
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )
        return str(dsn)


settings = Settings()
