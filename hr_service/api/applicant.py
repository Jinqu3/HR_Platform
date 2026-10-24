from uuid import UUID

from fastapi import APIRouter, Body

from hr_service.api.dependencies import DBDep
from schemas.applicant import ApplicantCreate, ApplicantPatch, ApplicantUpdate
from service.applicant import ApplicantService

router = APIRouter(prefix="/applicant", tags=["applicant"])


@router.get("/")
async def get_applicants(db: DBDep):
    applicants = await ApplicantService(db).get_applicants()
    return {"data": applicants}


@router.get("/{id}")
async def get_applicant(id: UUID, db: DBDep):
    applicant = await ApplicantService(db).get_applicant(applicant_id=id)
    return {"data": applicant}


@router.post("/")
async def create_applicant(db: DBDep, data: ApplicantCreate = Body()):  # noqa: B008
    applicant = await ApplicantService(db).create_applicant(data=data)
    return {"data": applicant}


@router.put("/{id}")
async def update_applicant(db: DBDep, id: UUID, data: ApplicantUpdate = Body()):  # noqa: B008
    applicant = await ApplicantService(db).update_applicant(applicant_id=id, data=data)
    return {"data": applicant}


@router.delete("/{id}")
async def delete_applicant(db: DBDep, id: UUID):
    await ApplicantService(db).delete_applicant(applicant_id=id)
    return {"status": "ok"}


@router.patch("/{id}")
async def patch_applicant(db: DBDep, id: UUID, data: ApplicantPatch = Body()):  # noqa: B008
    applicant = await ApplicantService(db).patch_applicant(applicant_id=id, data=data)
    return {"data": applicant}
