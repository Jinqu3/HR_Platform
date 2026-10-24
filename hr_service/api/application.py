from uuid import UUID

from celery.result import AsyncResult
from fastapi import APIRouter, Body, File, Form, HTTPException, UploadFile

from hr_service.api.dependencies import DBDep
from schemas.application import ApplicationCreate, ApplicationPatch
from service.application import ApplicationService
from utils.celery_app import celery_app
from utils.redis_client import redis_client

router = APIRouter(prefix="/application", tags=["application"])


@router.get("/")
async def get_applications(db: DBDep, company_id: UUID | None = None):
    applications = await ApplicationService(db).get_applications(company_id=company_id)
    return {"data": applications}


@router.get("/{id}")
async def get_application(id: UUID, db: DBDep):
    application = await ApplicationService(db).get_application(application_id=id)
    return {"data": application}


@router.get("/progress/{batch_id}")
async def get_batch_progress(batch_id: str, db: DBDep):
    progress = await ApplicationService(db).get_batch_progress(batch_id=batch_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Batch progress not found")
    return {"data": progress}


@router.get("/{id}/status")
async def get_application_status(id: UUID):
    task_id = redis_client.get(f"app:{id}:task_id")
    if not task_id:
        raise HTTPException(status_code=404, detail="Task not found for this application")

    task_result = AsyncResult(id=task_id, app=celery_app)
    return {
        "application_id": id,
        "task_id": task_id,
        "status": task_result.state,
        "result": task_result.result if task_result.ready() else None,
    }


@router.post("/{company_id}")
async def analyze_cv(company_id: UUID, db: DBDep):
    data = await ApplicationService(db).analyze_applications(company_id=company_id)
    return {"data": data}


@router.post("/")
async def create_application(
    db: DBDep,
    file: UploadFile = File(...),  # noqa: B008
    applicant_id: UUID = Form(...),  # noqa: B008
    vacancy_id: UUID = Form(...),  # noqa: B008
):
    try:
        application_data = ApplicationCreate(
            applicant_id=applicant_id, vacancy_id=vacancy_id
        )
    except Exception as e:  # noqa: BLE001
        raise HTTPException(
            status_code=422, detail=f"Invalid JSON in 'data' field: {e}"
        )
    application = await ApplicationService(db).create_application(
        file_obj=file, data=application_data
    )
    return {"data": application}


@router.patch("/{id}")
async def patch_application(
    db: DBDep, id: UUID, data: ApplicationPatch = Body()  # noqa: B008
):
    application = await ApplicationService(db).patch_application(
        application_id=id, data=data
    )
    return {"data": application}


@router.post("/{id}/analyze")
async def analyze_single_application(id: UUID, db: DBDep):
    try:
        result = await ApplicationService(db).analyze_single_application(application_id=id)
        return {"data": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{id}/download")
async def download_resume(id: UUID, db: DBDep):
    url = await ApplicationService(db).get_resume_download_url(application_id=id)
    if not url:
        raise HTTPException(status_code=404, detail="Resume file not found in storage")
    return {"data": {"download_url": url}}
