import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
import io
from fastapi.testclient import TestClient

from hr_service.main import app
from hr_service.api.dependencies import get_db
from hr_service.repository.base import BaseRepository
from hr_service.models.company import Company
from hr_service.utils.db_manager import DBManager
from hr_service.utils.s3_client import S3Client
from hr_service.service.application import ApplicationService


class DummyObj:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


@pytest.fixture
def client():
    uid = uuid4()
    db_mock = MagicMock(spec=DBManager)
    for name in ["companies", "vacancies", "applicants", "recruiters", "applications"]:
        repo = MagicMock()
        repo.get_all = AsyncMock(return_value=[])
        repo.get_one_or_none = AsyncMock(return_value=DummyObj(
            id=uid, company_id=uid, vacancy_id=uid, task_id=uid, applicant_id=uid,
            title="Dev", stack="Python", experience=2.0, requirements="Req", salary=100,
            evaluation_score=9.0, status="new"
        ))
        repo.add = AsyncMock(return_value=DummyObj(
            id=uid, title="Test", full_name="Test", email="t@t.com", phone="1",
            company_id=uid, vacancy_id=uid, applicant_id=uid,
            stack="Python", experience=2.0, requirements="Req", salary=100,
            evaluation_score=9.0, status="new"
        ))
        repo.delete = AsyncMock(return_value=None)
        repo.update = AsyncMock(return_value=None)
        setattr(db_mock, name, repo)

    db_mock.commit = AsyncMock(return_value=None)
    db_mock.rollback = AsyncMock(return_value=None)
    db_mock.__aenter__ = AsyncMock(return_value=db_mock)
    db_mock.__aexit__ = AsyncMock(return_value=None)

    app.dependency_overrides[get_db] = lambda: db_mock
    c = TestClient(app)
    yield c
    app.dependency_overrides.clear()


def test_all_api_routes(client):
    uid = uuid4()

    # Company routes
    assert client.get("/company/").status_code == 200
    assert client.get(f"/company/{uid}").status_code == 200
    assert client.post("/company/", json={"title": "T", "is_active": True}).status_code == 200
    assert client.put(f"/company/{uid}", json={"title": "T", "is_active": True}).status_code == 200
    assert client.patch(f"/company/{uid}", json={"title": "T"}).status_code == 200
    assert client.delete(f"/company/{uid}").status_code == 200

    # Vacancy routes
    assert client.get("/vacancy/").status_code == 200
    assert client.get(f"/vacancy/{uid}").status_code == 200
    assert client.post("/vacancy/", json={"title": "V", "stack": "S", "experience": 1.0, "requirements": "R", "salary": 100, "is_active": True, "company_id": str(uid)}).status_code == 200
    assert client.put(f"/vacancy/{uid}", json={"title": "V", "stack": "S", "experience": 1.0, "requirements": "R", "salary": 100, "is_active": True, "company_id": str(uid)}).status_code == 200
    assert client.patch(f"/vacancy/{uid}", json={"salary": 200}).status_code == 200
    assert client.delete(f"/vacancy/{uid}").status_code == 200

    # Applicant routes
    assert client.get("/applicant/").status_code == 200
    assert client.get(f"/applicant/{uid}").status_code == 200
    assert client.post("/applicant/", json={"full_name": "A", "email": "a@a.com", "phone": "1"}).status_code == 200
    assert client.put(f"/applicant/{uid}", json={"full_name": "A", "email": "a@a.com", "phone": "1"}).status_code == 200
    assert client.patch(f"/applicant/{uid}", json={"phone": "2"}).status_code == 200
    assert client.delete(f"/applicant/{uid}").status_code == 200

    # Recruiter routes
    assert client.get("/recruiter/").status_code == 200
    assert client.get(f"/recruiter/{uid}").status_code == 200
    assert client.post("/recruiter/", json={"full_name": "R", "email": "r@r.com", "company_id": str(uid), "is_active": True}).status_code == 200
    assert client.put(f"/recruiter/{uid}", json={"full_name": "R", "email": "r@r.com", "company_id": str(uid), "is_active": True}).status_code == 200
    assert client.patch(f"/recruiter/{uid}", json={"is_active": False}).status_code == 200
    assert client.delete(f"/recruiter/{uid}").status_code == 200

    # Application routes
    assert client.get("/application/").status_code == 200
    assert client.get(f"/application/{uid}").status_code == 200

    with patch("hr_service.utils.redis_client.redis_client.get", return_value=None):
        assert client.get(f"/application/{uid}/status").status_code == 404

    with patch("hr_service.utils.redis_client.redis_client.get", return_value=str(uuid4())), \
         patch("celery.result.AsyncResult") as mock_ar:
        mock_ar.return_value = MagicMock(state="SUCCESS", ready=lambda: True, result="ok")
        res = client.get(f"/application/{uid}/status")
        assert res.status_code in (200, 404)

    with patch("hr_service.service.application.ApplicationService.analyze_applications", new_callable=AsyncMock, return_value={"analyzed": 1}):
        assert client.post(f"/application/{uid}").status_code == 200

    files = {"file": ("test.zip", b"content", "application/zip")}
    data = {"applicant_id": str(uid), "vacancy_id": str(uid)}
    with patch("hr_service.utils.s3_client.S3Client.upload_fileobj", new_callable=AsyncMock), \
         patch("hr_service.utils.celery_app.celery_app.send_task") as mock_celery:
        mock_celery.return_value = DummyObj(id=str(uuid4()))
        assert client.post("/application/", files=files, data=data).status_code == 200

    assert client.patch(f"/application/{uid}", json={"evaluation_score": 9.0}).status_code == 200
    assert client.delete(f"/application/{uid}").status_code == 200


@pytest.mark.asyncio
async def test_repository_s3_dbmanager_dependencies():
    mock_session = AsyncMock()
    mock_session.execute = AsyncMock(return_value=MagicMock(scalars=MagicMock(return_value=MagicMock(all=lambda: [], first=lambda: None))))
    
    repo = BaseRepository(mock_session)
    repo.model = Company

    await repo.add(MagicMock(model_dump=lambda **kwargs: {"title": "Test"}))
    await repo.get_all()
    await repo.get_one_or_none()
    await repo.delete()
    await repo.update(data=MagicMock(model_dump=lambda **kwargs: {"title": "Test"}))

    s3 = S3Client("bucket")
    s3.client = MagicMock()
    s3.client.head_bucket = MagicMock()
    s3.client.upload_fileobj = MagicMock()
    s3.client.download_file = MagicMock()

    s3.ensure_bucket_exists()

    mock_file = MagicMock()
    mock_file.seek = AsyncMock()
    mock_file.read = AsyncMock(return_value=b"content")

    await s3.upload_fileobj(mock_file, "key", "file.zip")
    s3.download_file("key", "path.zip")

    # Test DBManager
    session_factory = MagicMock(return_value=mock_session)
    async with DBManager(session_factory) as dbm:
        assert dbm is not None
        await dbm.commit()
        await dbm.rollback()

    # Test get_db dependency
    async for db in get_db():
        assert db is not None
        break

    # Test ApplicationService batch progress
    app_service = ApplicationService(mock_session)
    with patch("hr_service.utils.redis_client.redis_client.hgetall", return_value={"total": "5", "current": "2", "status": "processing"}):
        prog = await app_service.get_batch_progress("batch123")
        assert prog["total"] == 5
        assert prog["current"] == 2
