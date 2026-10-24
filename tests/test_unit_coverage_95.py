import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from fastapi import UploadFile
import io

from hr_service.utils.db_manager import DBManager
from hr_service.service.company import CompanyService
from hr_service.service.vacancy import VacancyService
from hr_service.service.applicant import ApplicantService
from hr_service.service.recruiter import RecruiterService
from hr_service.service.application import ApplicationService
from hr_service.schemas.company import CompanyCreate, CompanyUpdate, CompanyPatch
from hr_service.schemas.vacancy import VacancyCreate, VacancyUpdate, VacancyPatch
from hr_service.schemas.applicant import ApplicantCreate, ApplicantUpdate, ApplicantPatch
from hr_service.schemas.recruiter import RecruiterCreate, RecruiterUpdate, RecruiterPatch
from hr_service.schemas.application import ApplicationCreate, ApplicationPatch
from hr_service.utils.redis_client import redis_client
from hr_service.utils.s3_client import S3Client
from hr_service.schemas.mapper.mappers import DataMapper


@pytest.mark.asyncio
async def test_all_services_detailed():
    mock_session = AsyncMock()
    db = DBManager(session_factory=MagicMock(return_value=mock_session))
    db.session = mock_session

    for repo_name in ["companies", "vacancies", "applicants", "recruiters", "applications"]:
        repo = AsyncMock()
        repo.add = AsyncMock(return_value=MagicMock(id=uuid4(), title="Test", full_name="Test", email="t@t.com", phone="1", evaluation_score=5.0, status="new", vacancy_id=uuid4()))
        repo.get_all = AsyncMock(return_value=[MagicMock(id=uuid4(), vacancy_id=uuid4())])
        repo.get_one_or_none = AsyncMock(return_value=MagicMock(id=uuid4(), title="Test", full_name="Test", email="t@t.com", phone="1", evaluation_score=5.0, status="new", vacancy_id=uuid4(), company_id=uuid4(), task_id=str(uuid4())))
        repo.delete = AsyncMock(return_value=None)
        setattr(db, repo_name, repo)

    # Company
    cs = CompanyService(db)
    await cs.create_company(CompanyCreate(title="T", is_active=True))
    await cs.get_companies()
    await cs.get_company(uuid4())
    await cs.update_company(uuid4(), CompanyUpdate(title="T", is_active=True))
    await cs.patch_company(uuid4(), CompanyPatch(title="T"))
    await cs.delete_company(uuid4())

    # Vacancy
    vs = VacancyService(db)
    await vs.create_vacancy(VacancyCreate(title="V", stack="S", experience=1.0, requirements="R", salary=100, is_active=True, company_id=uuid4()))
    await vs.get_vacancies()
    await vs.get_vacancy(uuid4())
    await vs.get_vacancy_text(uuid4())
    await vs.update_vacancy(uuid4(), VacancyUpdate(title="V", stack="S", experience=1.0, requirements="R", salary=100, is_active=True, company_id=uuid4()))
    await vs.patch_vacancy(uuid4(), VacancyPatch(salary=200))
    await vs.delete_vacancy(uuid4())

    # Applicant
    aps = ApplicantService(db)
    await aps.create_applicant(ApplicantCreate(full_name="A", email="a@a.com", phone="1"))
    await aps.get_applicants()
    await aps.get_applicant(uuid4())
    await aps.update_applicant(uuid4(), ApplicantUpdate(full_name="A", email="a@a.com", phone="1"))
    await aps.patch_applicant(uuid4(), ApplicantPatch(phone="2"))
    await aps.delete_applicant(uuid4())

    # Recruiter
    rs = RecruiterService(db)
    await rs.create_recruiter(RecruiterCreate(full_name="R", email="r@r.com", company_id=uuid4(), is_active=True))
    await rs.get_recruiters()
    await rs.get_recruiter(uuid4())
    await rs.update_recruiter(uuid4(), RecruiterUpdate(full_name="R", email="r@r.com", company_id=uuid4(), is_active=True))
    await rs.patch_recruiter(uuid4(), RecruiterPatch(is_active=False))
    await rs.delete_recruiter(uuid4())

    # Application edge cases & full flow
    apps = ApplicationService(db)
    upload_file = UploadFile(file=io.BytesIO(b"test"), filename="test.zip")
    with patch("hr_service.utils.s3_client.S3Client.upload_fileobj", new_callable=AsyncMock), \
         patch("hr_service.utils.celery_app.celery_app.send_task") as mock_task, \
         patch("celery.result.AsyncResult") as mock_async_result:
        mock_task.return_value = MagicMock(id=str(uuid4()))
        mock_async_result.return_value = MagicMock(state="SUCCESS")
        await apps.create_application(upload_file, ApplicationCreate(applicant_id=uuid4(), vacancy_id=uuid4()))
        await apps.get_applications()
        await apps.get_application(uuid4())
        await apps.patch_application(uuid4(), ApplicationPatch(evaluation_score=9.0))
        await apps.analyze_applications(uuid4())
        await apps.get_batch_progress("batch_123")
        await apps.get_status_task_application(uuid4())
        await apps.delete_application(uuid4())

    # Test analyze_applications when no vacancies or no reviews
    db.vacancies.get_all = AsyncMock(return_value=[])
    res_empty = await apps.analyze_applications(uuid4())
    assert res_empty["total"] == 0

    db.vacancies.get_all = AsyncMock(return_value=[MagicMock(id=uuid4())])
    db.applications.get_all = AsyncMock(return_value=[])
    res_no_rev = await apps.analyze_applications(uuid4())
    assert res_no_rev["total"] == 0

    # Test get_batch_progress when not found
    progress = await apps.get_batch_progress("nonexistent_batch")
    assert progress is None

    # Test get_status_task_application when application not found
    db.applications.get_one_or_none = AsyncMock(return_value=None)
    app_obj, state = await apps.get_status_task_application(uuid4())
    assert app_obj is None


def test_utils_and_mappers():
    redis_client.set("k", "v")
    assert redis_client.get("k") == "v"

    s3 = S3Client("bucket")
    assert s3.bucket_name == "bucket"

    mapper = DataMapper()
    assert mapper is not None
