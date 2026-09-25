from uuid import UUID as uuid, uuid4


from config import settings  # type: ignore
from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import (  # type: ignore
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column  # type: ignore

engine = create_async_engine(settings.DB_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    id: Mapped[uuid] = mapped_column(
        UUID(as_uuid=True),
        default=uuid4,
        primary_key=True,
    )
