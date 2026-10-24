from typing import Annotated

from fastapi import Depends

from hr_service.database import async_session
from utils.db_manager import DBManager


async def get_db():
    async with DBManager(session_factory=async_session) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]