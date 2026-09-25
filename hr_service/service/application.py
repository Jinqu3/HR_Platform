from uuid import UUID

from hr_service.schemas.application import ApplicationCreate, ApplicationPatch, ApplicationUpdate
from hr_service.service.base import BaseService


class ApplicationService(BaseService):

    async def create_application(self, data: ApplicationCreate):
        application = await self.db.applications.add(data)
        await self.db.commit()
        return application

    async def get_application(self, application_id: UUID):
        return await self.db.applications.get_one_or_none(id=application_id)

    async def get_applications(self):
        return await self.db.applications.get_all()

    async def update_application(self, application_id: UUID, data: ApplicationUpdate):
        await self.db.applications.update(data, is_patch=False, id=application_id)
        await self.db.commit()
        return await self.get_application(application_id)

    async def patch_application(self, application_id: UUID, data: ApplicationPatch):
        await self.db.applications.update(data, is_patch=True, id=application_id)
        await self.db.commit()
        return await self.get_application(application_id)

    async def delete_application(self, application_id: UUID):
        await self.db.applications.delete(id=application_id)
        await self.db.commit()
