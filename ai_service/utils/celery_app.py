from celery import Celery

from ai_service.config import settings

celery_app = Celery(
    settings.CELERY_NAME,
    broker=settings.CELERY_RABBIT_BROKER_URL,
    backend=settings.CELERY_REDIS_BACKEND_URL,
    include=[
        "ai_service.tasks.unzip",
        "ai_service.tasks.parse",
        "ai_service.tasks.evaluate",
    ],
)

celery_app.conf.update(
    # Настройки сериализации
    task_serializer="json",  # Формат сериализации задач
    accept_content=["json"],  # Принимаемые форматы данных
    result_serializer="json",  # Формат сериализации результатов

    enable_utc=True,  # Использовать UTC для внутренних операций

    # Настройки отслеживания
    task_track_started=True,  # Отслеживать начало выполнения задач
    task_ignore_result=False,  # Сохранять результаты задач
    result_extended=True,

    # Настройки таймаутов
    task_time_limit=30 * 60,  # Максимальное время выполнения задачи (30 минут)
    task_soft_time_limit=25 * 60,  # Мягкий таймаут (25 минут)

    # Настройки воркера
    worker_prefetch_multiplier=1,  # Количество задач, которые воркер берёт одновременно
    worker_max_tasks_per_child=1000,  # Максимальное количество задач на дочерний процесс

    # Настройки повторных попыток
    task_acks_late=True,  # Подтверждать выполнение задачи только после успешного завершения
    worker_disable_rate_limits=False,  # Не отключать ограничения скорости
    # Настройки логирования
    worker_log_format="[%(asctime)s: %(levelname)s/%(processName)s] %(message)s",
    worker_task_log_format="[%(asctime)s: %(levelname)s/%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s",
)
