FROM python:3.12-slim

WORKDIR /app

COPY ai_service/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ai_service ./ai_service

CMD ["celery", "--app=ai_service.utils.celery_app:celery_app", "worker", "--pool=gevent", "--concurrency=20", "-l", "INFO"]
