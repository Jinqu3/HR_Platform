from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str

    CELERY_NAME: str
    CELERY_BROKER_USER: str
    CELERY_BROKER_PASSWORD: str
    CELERY_BROKER_HOST: str
    CELERY_BROKER_PORT: str

    CELERY_BACKEND_HOST: str
    CELERY_BACKEND_PORT: str

    S3_BUCKET_URL: str
    S3_BUCKET_NAME: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def CELERY_RABBIT_BROKER_URL(self):
        return f"amqp://{self.CELERY_BROKER_USER}:{self.CELERY_BROKER_PASSWORD}@{self.CELERY_BROKER_HOST}:{self.CELERY_BROKER_PORT}//"

    @property
    def CELERY_REDIS_BACKEND_URL(self):
        return f"redis://{self.CELERY_BACKEND_HOST}:{self.CELERY_BACKEND_PORT}/0"

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    @property
    def DB_URL_SYNC(self):
        return f"postgresql+psycopg2://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    model_config = SettingsConfigDict(
        env_file=(str(Path(__file__).parent / ".env"), "hr_service/.env", ".env"),
        extra='ignore'
    )

settings = Settings()  # type: ignore
