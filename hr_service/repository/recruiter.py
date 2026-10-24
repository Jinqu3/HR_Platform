from sqlalchemy import insert, select
from pydantic import BaseModel

from hr_service.models.recruiter import Recruiter
from hr_service.repository.base import BaseRepository
from schemas.mapper.mappers import RecruiterMapper
from hr_service.utils.auth_utils import hash_password


class RecruiterRepository(BaseRepository):
    model = Recruiter
    mapper = RecruiterMapper

    async def add(self, data: BaseModel):
        data_dict = data.model_dump()
        password = data_dict.pop("password", None)
        if password:
            data_dict["hashed_password"] = hash_password(password)
        stmt = insert(self.model).values(**data_dict).returning(self.model)
        result = await self.session.execute(stmt)
        res = result.scalars().one()
        return self.mapper.map_to_domain_entity(res) if self.mapper else res

    async def get_model_by_email(self, email: str):
        stmt = select(self.model).filter_by(email=email)
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()
