from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from hr_service.schemas.mapper.base import DataMapper


class BaseRepository:
    model = None
    mapper: type[DataMapper] | None = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_one_or_none(self, *filter, **filter_by):
        stmt = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        res = result.scalars().one_or_none()
        if res is None:
            return None
        return self.mapper.map_to_domain_entity(res) if self.mapper else res

    async def get_all(self, *filter, **filter_by):
        stmt = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        return [self.mapper.map_to_domain_entity(res) for res in items]

    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        res = result.scalars().one()
        return self.mapper.map_to_domain_entity(res) if self.mapper else res

    async def delete(self, *filter, **filter_by):
        if not await self.get_one(*filter, **filter_by):
            raise NoResultFound

        stmt = delete(self.model).filter(*filter).filter_by(**filter_by)
        await self.session.execute(stmt)

    async def update(
        self, data: BaseModel, is_patch: bool = False, *filter, **filter_by
    ):
        if not await self.get_one(*filter, **filter_by):
            raise NoResultFound

        stmt = (
            update(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=is_patch))
        )
        await self.session.execute(stmt)
