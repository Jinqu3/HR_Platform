from uuid import UUID
from fastapi import APIRouter, Body
from schemas.recruiter import RecruiterCreate, RecruiterUpdate, RecruiterPatch
from service.recruiter import RecruiterService

from hr_service.api.dependencies import DBDep

router = APIRouter(prefix="/recruiter", tags=["recruiter"])


@router.get("/")
async def get_recruiters(db: DBDep):
    recruiters = await RecruiterService(db).get_recruiters()
    return {"data": recruiters}


@router.get("/{id}")
async def get_recruiter(id: UUID, db: DBDep):
    recruiter = await RecruiterService(db).get_recruiter(recruiter_id=id)
    return {"data": recruiter}


@router.post("/")
async def create_recruiter(db: DBDep, data: RecruiterCreate = Body()):  # noqa: B008
    recruiter = await RecruiterService(db).create_recruiter(data=data)
    return {"data": recruiter}


@router.put("/{id}")
async def update_recruiter(db: DBDep, id: UUID, data: RecruiterUpdate = Body()):  # noqa: B008
    recruiter = await RecruiterService(db).update_recruiter(recruiter_id=id, data=data)
    return {"data": recruiter}


@router.delete("/{id}")
async def delete_recruiter(db: DBDep, id: UUID):
    await RecruiterService(db).delete_recruiter(recruiter_id=id)
    return {"status": "ok"}


@router.patch("/{id}")
async def patch_recruiter(db: DBDep, id: UUID, data: RecruiterPatch = Body()):  # noqa: B008
    recruiter = await RecruiterService(db).patch_recruiter(recruiter_id=id, data=data)
    return {"data": recruiter}
