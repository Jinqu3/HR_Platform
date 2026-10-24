import os
import asyncio
import sys

if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

import pytest
from testcontainers.community.postgres import PostgresContainer
from testcontainers.community.redis import RedisContainer
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from httpx import AsyncClient, ASGITransport

# Start Testcontainers for Postgres and Redis (Session-scoped)
postgres_container = PostgresContainer("postgres:15-alpine")
postgres_container.start()

redis_container = RedisContainer("redis:7-alpine")
redis_container.start()

db_url_async = postgres_container.get_connection_url(driver="asyncpg")
db_url_sync = postgres_container.get_connection_url(driver="psycopg2")
redis_host = redis_container.get_container_host_ip()
redis_port = redis_container.get_exposed_port(6379)

os.environ["DATABASE_NAME"] = postgres_container.dbname
os.environ["DATABASE_USER"] = postgres_container.username
os.environ["DATABASE_PASSWORD"] = postgres_container.password
os.environ["DATABASE_HOST"] = postgres_container.get_container_host_ip()
os.environ["DATABASE_PORT"] = str(postgres_container.get_exposed_port(5432))

os.environ["CELERY_NAME"] = "test_celery"
os.environ["CELERY_BROKER_USER"] = "guest"
os.environ["CELERY_BROKER_PASSWORD"] = "guest"
os.environ["CELERY_BROKER_HOST"] = "localhost"
os.environ["CELERY_BROKER_PORT"] = "5672"
os.environ["CELERY_BACKEND_HOST"] = redis_host
os.environ["CELERY_BACKEND_PORT"] = str(redis_port)
os.environ["CELERY_BACKEND_PASSWORD"] = ""
os.environ["S3_BUCKET_URL"] = "http://localhost:9000"
os.environ["S3_BUCKET_NAME"] = "test-bucket"
os.environ["S3_ACCESS_KEY"] = "access"
os.environ["S3_SECRET_KEY"] = "secret"
os.environ["JWT_SECRET_KEY"] = "test_secret_key"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"

import hr_service.database
from hr_service.main import app
from hr_service.database import Base

# Initialize tables synchronously once per session
sync_engine = create_engine(db_url_sync)
Base.metadata.create_all(bind=sync_engine)
sync_engine.dispose()


@pytest.fixture(autouse=True)
async def isolate_database():
    async_engine = create_async_engine(db_url_async, echo=False, poolclass=NullPool)
    async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)

    hr_service.database.engine = async_engine
    hr_service.database.async_session = async_session_maker

    yield

    await async_engine.dispose()


@pytest.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
