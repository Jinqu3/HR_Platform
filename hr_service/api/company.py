from uuid import UUID

from fastapi import APIRouter, Body

from hr_service.api.dependencies import DBDep
from schemas.company import CompanyCreate, CompanyPatch, CompanyUpdate
from service.company import CompanyService

router = APIRouter(prefix="/company", tags=["company"])


@router.get("/")
async def get_companies(db: DBDep):
    companies = await CompanyService(db).get_companies()
    return {"data": companies}


@router.get("/{id}")
async def get_company(id: UUID, db: DBDep):
    company = await CompanyService(db).get_company(company_id=id)
    return {"data": company}


@router.post("/")
async def create_company(db: DBDep, data: CompanyCreate = Body()):  # noqa: B008
    company = await CompanyService(db).create_company(data=data)
    return {"data": company}


@router.put("/{id}")
async def update_company(db: DBDep, id: UUID, data: CompanyUpdate = Body()):  # noqa: B008
    company = await CompanyService(db).update_company(company_id=id, data=data)
    return {"data": company}


@router.delete("/{id}")
async def delete_company(db: DBDep, id: UUID):
    await CompanyService(db).delete_company(company_id=id)
    return {"status": "ok"}


@router.patch("/{id}")
async def patch_company(db: DBDep, id: UUID, data: CompanyPatch = Body()):  # noqa: B008
    company = await CompanyService(db).patch_company(company_id=id, data=data)
    return {"data": company}
