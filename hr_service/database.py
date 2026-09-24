from uuid import uuid4

from config import settings  # type: ignore
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine # type: ignore
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column # type: ignore

engine = create_async_engine(settings.DB_URL, echo=True)
session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(default=uuid4(), autoincrement=False, primary_key=True)
