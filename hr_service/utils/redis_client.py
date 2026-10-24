import redis
from hr_service.config import settings

redis_client = redis.Redis.from_url(
    settings.CELERY_REDIS_BACKEND_URL, decode_responses=True
)
