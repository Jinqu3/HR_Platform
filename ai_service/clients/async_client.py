import logging

import httpx

logger = logging.getLogger(__name__)


async def send_request(url: str, method:str, data: dict) -> dict:
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            if method == "GET":
                response = await client.get(url)
            elif method == "POST":
                response = await client.post(url, json=data)
            elif method == "PUT":
                response = await client.put(url, json=data)
            elif method == "DELETE":
                response = await client.delete(url)
            elif method == "PATCH":
                response = await client.patch(url, json=data)

            response.raise_for_status()

            return response.json()

        except httpx.HTTPStatusError as e:
            logger.error(
                f"Ошибка сохранения в БД: {e.response.status_code} - {e.response.text}"
            )
            raise
        except httpx.RequestError as e:
            logger.error(f"Ошибка сети при обращении к сервису БД: {e}")
            raise
