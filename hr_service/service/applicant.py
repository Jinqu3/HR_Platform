from uuid import UUID

from hr_service.schemas.applicant import (
    ApplicantCreate,
    ApplicantPatch,
    ApplicantUpdate,
)
from hr_service.service.base import BaseService


class ApplicantService(BaseService):

    async def create_applicant(self, data: ApplicantCreate):
        applicant = await self.db.applicants.add(data)
        await self.db.commit()
        return applicant

    async def get_applicant(self, applicant_id: UUID):
        return await self.db.applicants.get_one_or_none(id=applicant_id)

    async def get_applicants(self):
        return await self.db.applicants.get_all()

    async def update_applicant(self, applicant_id: UUID, data: ApplicantUpdate):
        await self.db.applicants.update(data, is_patch=False, id=applicant_id)
        await self.db.commit()
        return await self.get_applicant(applicant_id)

    async def patch_applicant(self, applicant_id: UUID, data: ApplicantPatch):
        await self.db.applicants.update(data, is_patch=True, id=applicant_id)
        await self.db.commit()
        return await self.get_applicant(applicant_id)

    async def delete_applicant(self, applicant_id: UUID):
        await self.db.applicants.delete(id=applicant_id)
        await self.db.commit()
