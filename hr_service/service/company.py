from uuid import UUID

from hr_service.schemas.company import CompanyCreate, CompanyPatch, CompanyUpdate
from hr_service.service.base import BaseService


class CompanyService(BaseService):

    async def create_company(self, data: CompanyCreate):
        company = await self.db.companies.add(data)
        await self.db.commit()
        return company

    async def get_company(self, company_id: UUID):
        return await self.db.companies.get_one_or_none(id=company_id)

    async def get_companies(self):
        return await self.db.companies.get_all()

    async def update_company(self, company_id: UUID, data: CompanyUpdate):
        await self.db.companies.update(data, is_patch=False, id=company_id)
        await self.db.commit()
        return await self.get_company(company_id)

    async def patch_company(self, company_id: UUID, data: CompanyPatch):
        await self.db.companies.update(data, is_patch=True, id=company_id)
        await self.db.commit()
        return await self.get_company(company_id)

    async def delete_company(self, company_id: UUID):
        await self.db.companies.delete(id=company_id)
        await self.db.commit()
