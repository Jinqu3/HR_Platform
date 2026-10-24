FROM python:3.12-slim

WORKDIR /app

COPY hr_service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY hr_service ./hr_service
COPY frontend ./frontend

CMD ["uvicorn", "hr_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
