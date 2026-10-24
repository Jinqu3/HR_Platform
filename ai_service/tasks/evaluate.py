import asyncio
import json
import re

from celery import chain
from celery.exceptions import Ignore
from loguru import logger
from openai import OpenAIError

from ai_service.clients.async_client import send_request
from ai_service.clients.llm_client import get_client
from ai_service.config import settings
from ai_service.prompts.evaluate_text import EVALUATE_PROMPT
from ai_service.utils.celery_app import celery_app


@celery_app.task(name="evaluate_cv_chain_task")
def evaluate_cv_chain_task(application_id: str, s3_key: str, vacancy_text: str, batch_id: str = None):
    workflow = chain(
        celery_app.signature(
            "unzip_cv_task",
            args=[application_id, s3_key],
        ),
        celery_app.signature("parse_cv_task",
                             args=[application_id],),
        celery_app.signature("evaluate_cv_task", args=[application_id, vacancy_text, batch_id]),
    )
    return workflow.apply_async()


@celery_app.task(
    name='evaluate_cv_task',
    autoretry_for=(OpenAIError,),
    max_retries=3,
    retry_backoff=True,
    retry_backoff_max=60,
    retry_jitter=True
)
def evaluate_cv_task(structurized_data: str, application_id: str, vacancy_text: str, batch_id: str = None):
    try:
        prompt = (
            EVALUATE_PROMPT.replace("{vacancy_text}", str(vacancy_text))
            + f"\n\nСтруктурированные данные резюме:\n{structurized_data}\n\n"
            "Верни ответ строго в формате JSON с полями 'evaluated_text' (текст анализа) и 'evaluation_score' (число от 0 до 100)."
        )

        try:
            with get_client() as client:
                response = client.chat.completions.create(
                    model=settings.AI_MODEL,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                )
        except OpenAIError as e:
            logger.error(e)
            asyncio.run(
                send_request(
                    url=f"{settings.HR_SERVICE_URL}/application/{application_id}",
                    method="PATCH",
                    data={"status": "error"},
                )
            )
            raise Ignore("Ошибка запроса к LLM")

        raw_content = response.choices[0].message.content
        cleaned_content = re.sub(r"^```(?:json)?\s*", "", raw_content.strip())
        cleaned_content = re.sub(r"\s*```$", "", cleaned_content)

        try:
            data = json.loads(cleaned_content)
            evaluated_text = data.get("evaluated_text") or data.get("text")
            evaluation_score = data.get("evaluation_score") or data.get("score")
        except json.JSONDecodeError:
            # Попытка починить обрезанный JSON: добавить недостающие закрывающие символы
            repaired = cleaned_content.rstrip()
            if not repaired.endswith("}"):
                # Ищем последнее валидное поле и закрываем объект
                repaired = repaired.rstrip(",") + "\n}"
            try:
                data = json.loads(repaired)
                evaluated_text = data.get("evaluated_text") or data.get("text")
                evaluation_score = data.get("evaluation_score") or data.get("score")
                logger.warning(f"JSON был обрезан, восстановлен для application {application_id}")
            except json.JSONDecodeError:
                # Fallback: вытащить поля через regex
                text_match = re.search(r'"evaluated_text"\s*:\s*"(.*?)(?:"|$)', cleaned_content, re.DOTALL)
                score_match = re.search(r'"evaluation_score"\s*:\s*([\d.]+)', cleaned_content)
                evaluated_text = text_match.group(1).replace('\\"', '"') if text_match else cleaned_content[:500]
                evaluation_score = float(score_match.group(1)) if score_match else None
                logger.warning(f"Невалидный JSON от модели, использован regex-fallback для application {application_id}")

        asyncio.run(
            send_request(
                url=f"{settings.HR_SERVICE_URL}/application/{application_id}",
                method='PATCH',
                data={
                    "status": "analyzed",
                    "evaluated_text": evaluated_text,
                    "evaluation_score": evaluation_score,
                },
            )
        )

    finally:
        if batch_id:
            try:
                import redis
                r = redis.Redis.from_url(settings.CELERY_REDIS_BACKEND_URL, decode_responses=True)
                current = r.hincrby(f"batch:{batch_id}:progress", "current", 1)
                total = int(r.hget(f"batch:{batch_id}:progress", "total") or 1)
                if current >= total:
                    r.hset(f"batch:{batch_id}:progress", "status", "completed")
            except Exception as ex:
                logger.error(f"Failed to increment progress in Redis for batch {batch_id}: {ex}")
