from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
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

    AI_TOKEN: str
    AI_CREDENTIALS: str
    AI_MODEL: str = "gpt-4o-mini"
    HR_SERVICE_URL: str

    @property
    def CELERY_RABBIT_BROKER_URL(self):
        return f"amqp://{self.CELERY_BROKER_USER}:{self.CELERY_BROKER_PASSWORD}@{self.CELERY_BROKER_HOST}:{self.CELERY_BROKER_PORT}//"

    @property
    def CELERY_REDIS_BACKEND_URL(self):
        return f"redis://{self.CELERY_BACKEND_HOST}:{self.CELERY_BACKEND_PORT}/0"

    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parent / ".env")

settings = Settings()  # type: ignore
