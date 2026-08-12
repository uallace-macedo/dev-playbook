from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    POSTGRES_USER: str = ''
    POSTGRES_PASSWORD: str = ''
    POSTGRES_DB: str = ''
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 6000

    DATABASE_URL: str = ''
    WEB_URL: str = ''

    @computed_field
    @property
    def sync_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL

        return f'postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}'

    JWT_SECRET_KEY: str = ''
    JWT_ALGORITHM: str = "HS256"
    TOKEN_EXPIRES_MINUTES: int = 30


settings = Settings()
