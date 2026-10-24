import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from utils.celery_app import celery_app

sys.path.append(str(Path(__file__).resolve().parent.parent))

from contextlib import asynccontextmanager

from hr_service.api.applicant import router as applicant_router
from hr_service.api.application import router as application_router
from hr_service.api.auth import router as auth_router
from hr_service.api.company import router as company_router
from hr_service.api.recruiter import router as recruiter_router
from hr_service.api.vacancy import router as vacancy_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        celery_app.control.inspect().active()
        print("Подключение к брокеру успешно!")
    except Exception as e:  # noqa: BLE001
        print(f"Ошибка подключения к брокеру: {e}")

    max_retries = 15
    retry_delay = 2
    for attempt in range(1, max_retries + 1):
        try:
            from hr_service.database import engine
            from sqlalchemy import text
            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            print("Успешное подключение к базе данных!")
            break
        except Exception as e:
            if attempt == max_retries:
                print(f"Не удалось подключиться к базе данных после {max_retries} попыток: {e}")
                raise
            print(f"Попытка {attempt}/{max_retries}: Ошибка подключения к БД ({e}). Повтор через {retry_delay} сек...")
            await asyncio.sleep(retry_delay)

    try:
        from alembic import command
        from alembic.config import Config
        alembic_ini_path = Path(__file__).resolve().parent / "alembic.ini"
        alembic_cfg = Config(str(alembic_ini_path))
        command.upgrade(alembic_cfg, "head")
        print("Миграции Alembic успешно применены.")
    except Exception as e:
        print(f"Ошибка при применении миграций Alembic: {e}")

    try:
        from hr_service.database import async_session
        from hr_service.models.company import Company
        from hr_service.seed_data import seed
        from sqlalchemy import select

        async with async_session() as session:
            result = await session.execute(select(Company).limit(1))
            company = result.scalars().first()
            if not company:
                print("База данных не содержит данных. Запуск сидинга...")
                await seed()
            else:
                print("Данные в базе данных уже существуют.")
    except Exception as e:
        print(f"Ошибка при проверке/сидинге данных: {e}")

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_path = Path(__file__).resolve().parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")


@app.get("/")
async def root():
    index_file = frontend_path / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "HR-Sieve API is running. Frontend not found."}


app.include_router(auth_router)
app.include_router(vacancy_router)
app.include_router(company_router)
app.include_router(application_router)
app.include_router(recruiter_router)
app.include_router(applicant_router)

if __name__ == '__main__':
    from hr_service.seed_data import *

    asyncio.run(seed())
    
    uvicorn.run("hr_service.main:app", host='0.0.0.0', port=8000)
