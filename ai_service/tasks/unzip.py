import os
import shutil
import zipfile
from uuid import UUID

from ai_service.clients.s3_client import S3Client
from ai_service.config import settings
from ai_service.utils.celery_app import celery_app


@celery_app.task(name='unzip_cv_task')
def unzip_cv_task(application_id: UUID, s3_key: str) -> str:
    local_archive_path = f"/tmp/applications/archives/{application_id}.zip"
    local_path = "/tmp/applications/archives"
    extract_to = "/tmp/applications/cvs"

    # Создаем родительские директории
    os.makedirs(local_path, exist_ok=True)
    os.makedirs(extract_to, exist_ok=True)

    # Скачиваем архив из S3
    S3Client(settings.S3_BUCKET_NAME).download_file(
        s3_key=s3_key, local_path=local_archive_path
    )

    with zipfile.ZipFile(local_archive_path, "r") as zip_ref:
        first_file = next(f for f in zip_ref.namelist() if not f.endswith("/"))
        _, ext = os.path.splitext(first_file)
        target_file_path = f"{extract_to}/{application_id}{ext}"
        with zip_ref.open(first_file) as src, open(target_file_path, "wb") as dst:
            shutil.copyfileobj(src, dst)

    os.remove(local_archive_path)

    # Возвращаем точный путь к файлу: /tmp/applications/cvs/<application_id>.[pdf,docx]
    return target_file_path
