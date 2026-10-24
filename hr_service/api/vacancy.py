from uuid import UUID

from fastapi import APIRouter, Body

from hr_service.api.dependencies import DBDep
from schemas.vacancy import VacancyCreate, VacancyPatch, VacancyUpdate
from service.vacancy import VacancyService

router = APIRouter(prefix="/vacancy", tags=["vacancy"])


@router.get("/")
async def get_vacancies(db: DBDep, company_id: UUID | None = None):
    vacancies = await VacancyService(db).get_vacancies(company_id=company_id)
    return {"data": vacancies}


@router.get("/{id}")
async def get_vacancy(id: UUID, db: DBDep):
    vacancy = await VacancyService(db).get_vacancy(vacancy_id=id)
    return {"data": vacancy}


@router.post("/")
async def create_vacancy(db: DBDep, data: VacancyCreate = Body()):  # noqa: B008
    vacancy = await VacancyService(db).create_vacancy(data=data)
    return {"data": vacancy}


@router.put("/{id}")
async def update_vacancy(db: DBDep, id: UUID, data: VacancyUpdate = Body()):  # noqa: B008
    vacancy = await VacancyService(db).update_vacancy(vacancy_id=id, data=data)
    return {"data": vacancy}


@router.delete("/{id}")
async def delete_vacancy(db: DBDep, id: UUID):
    await VacancyService(db).delete_vacancy(vacancy_id=id)
    return {"status": "ok"}


@router.patch("/{id}")
async def patch_vacancy(db: DBDep, id: UUID, data: VacancyPatch = Body()):  # noqa: B008
    vacancy = await VacancyService(db).patch_vacancy(vacancy_id=id, data=data)
    return {"data": vacancy}
