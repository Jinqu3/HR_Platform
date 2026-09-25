from uuid import UUID

from hr_service.schemas.recruiter import (
    RecruiterCreate,
    RecruiterPatch,
    RecruiterUpdate,
)
from hr_service.service.base import BaseService


class RecruiterService(BaseService):

    async def create_recruiter(self, data: RecruiterCreate):
        recruiter = await self.db.recruiters.add(data)
        await self.db.commit()
        return recruiter

    async def get_recruiter(self, recruiter_id: UUID):
        return await self.db.recruiters.get_one_or_none(id=recruiter_id)

    async def get_recruiters(self):
        return await self.db.recruiters.get_all()

    async def update_recruiter(self, recruiter_id: UUID, data: RecruiterUpdate):
        await self.db.recruiters.update(data, is_patch=False, id=recruiter_id)
        await self.db.commit()
        return await self.get_recruiter(recruiter_id)

    async def patch_recruiter(self, recruiter_id: UUID, data: RecruiterPatch):
        await self.db.recruiters.update(data, is_patch=True, id=recruiter_id)
        await self.db.commit()
        return await self.get_recruiter(recruiter_id)

    async def delete_recruiter(self, recruiter_id: UUID):
        await self.db.recruiters.delete(id=recruiter_id)
        await self.db.commit()
