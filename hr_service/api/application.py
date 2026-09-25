from uuid import UUID

from fastapi import APIRouter, Body
from schemas.application import ApplicationCreate, ApplicationPatch, ApplicationUpdate
from service.application import ApplicationService

from hr_service.api.dependencies import DBDep

router = APIRouter(prefix="/application", tags=["application"])


@router.get("/")
async def get_applications(db: DBDep):
    applications = await ApplicationService(db).get_applications()
    return {"data": applications}


@router.get("/{id}")
async def get_application(id: UUID, db: DBDep):
    application = await ApplicationService(db).get_application(application_id=id)
    return {"data": application}


@router.post("/")
async def create_application(db: DBDep, data: ApplicationCreate = Body()):  # noqa: B008
    application = await ApplicationService(db).create_application(data=data)
    return {"data": application}


@router.put("/{id}")
async def update_application(db: DBDep, id: UUID, data: ApplicationUpdate = Body()):  # noqa: B008
    application = await ApplicationService(db).update_application(application_id=id, data=data)
    return {"data": application}


@router.delete("/{id}")
async def delete_application(db: DBDep, id: UUID):
    await ApplicationService(db).delete_application(application_id=id)
    return {"status": "ok"}


@router.patch("/{id}")
async def patch_application(db: DBDep, id: UUID, data: ApplicationPatch = Body()):  # noqa: B008
    application = await ApplicationService(db).patch_application(application_id=id, data=data)
    return {"data": application}
