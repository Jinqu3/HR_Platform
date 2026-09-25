from uuid import UUID

from hr_service.schemas.vacancy import VacancyCreate, VacancyPatch, VacancyUpdate
from hr_service.service.base import BaseService


class VacancyService(BaseService):

    async def create_vacancy(self, data: VacancyCreate):
        vacancy = await self.db.vacancies.add(data)
        await self.db.commit()
        return vacancy

    async def get_vacancy(self, vacancy_id: UUID):
        return await self.db.vacancies.get_one_or_none(id=vacancy_id)

    async def get_vacancies(self):
        return await self.db.vacancies.get_all()

    async def update_vacancy(self, vacancy_id: UUID, data: VacancyUpdate):
        await self.db.vacancies.update(data, is_patch=False, id=vacancy_id)
        await self.db.commit()
        return await self.get_vacancy(vacancy_id)

    async def patch_vacancy(self, vacancy_id: UUID, data: VacancyPatch):
        await self.db.vacancies.update(data, is_patch=True, id=vacancy_id)
        await self.db.commit()
        return await self.get_vacancy(vacancy_id)

    async def delete_vacancy(self, vacancy_id: UUID):
        await self.db.vacancies.delete(id=vacancy_id)
        await self.db.commit()
