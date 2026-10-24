from contextlib import contextmanager

from openai import OpenAI

from ai_service.config import settings


@contextmanager
def get_client():
    with OpenAI(
    api_key=f"{settings.AI_TOKEN}",
    base_url=f"https://agent.timeweb.cloud/api/v1/cloud-ai/agents/{settings.AI_CREDENTIALS}/v1",
    ) as client:
        yield client
