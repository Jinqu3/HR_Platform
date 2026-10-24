import asyncio
import os
import mimetypes
from celery.exceptions import Ignore
from loguru import logger
from openai import OpenAIError
import pypdf
import docx

from ai_service.clients.async_client import send_request
from ai_service.clients.llm_client import get_client
from ai_service.config import settings
from ai_service.prompts.structurize_data import STRUCTURIZE_RESUME_PROMPT
from ai_service.utils.celery_app import celery_app


def extract_text_from_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    text = ""
    if ext == ".pdf":
        reader = pypdf.PdfReader(path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    elif ext in [".docx", ".doc"]:
        doc = docx.Document(path)
        for para in doc.paragraphs:
            if para.text:
                text += para.text + "\n"
    elif ext == ".txt":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    else:
        # Fallback на случай других форматов
        with open(path, "rb") as f:
            text = f.read().decode("utf-8", errors="ignore")
    return text.strip()


@celery_app.task(
    name='parse_cv_task',
    autoretry_for=(OpenAIError,),
    max_retries=3,
    retry_backoff=True,
    retry_backoff_max=60,
    retry_jitter=True
)
def parse_cv_task(path: str, application_id: str):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            logger.error(f"File not found: {path}")
            asyncio.run(
                send_request(
                    url=f"{settings.HR_SERVICE_URL}/application/{application_id}",
                    method="PATCH",
                    data={"status": "error", "error": "File not found"},
                )
            )
            raise Ignore("File not found")

        # Извлекаем текст из файла резюме
        resume_text = extract_text_from_file(path)
        if not resume_text:
            raise ValueError("Не удалось извлечь текст из файла резюме")

        # Формируем промпт с текстом резюме
        prompt = f"{STRUCTURIZE_RESUME_PROMPT}\n\nТекст резюме:\n{resume_text}"

        with get_client() as client:
            messages = [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
            response = client.chat.completions.create(
                model=settings.AI_MODEL,
                messages=messages,
            )

    except (OpenAIError, Exception) as e:
        logger.error(f"Ошибка при запросе к LLM или парсинге файла: {e}")
        asyncio.run(
            send_request(
                url=f"{settings.HR_SERVICE_URL}/application/{application_id}",
                method="PATCH",
                data={"status": "error"},
            )
        )
        raise Ignore("Ошибка при обработке резюме.")

    if response.choices and response.choices[0].message.content:
        return response.choices[0].message.content

    logger.error("Ошибка: модель вернула пустой ответ или неожиданный формат.")
    raise Ignore("Ошибка: модель вернула пустой ответ или неожиданный формат.")