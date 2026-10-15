from typing import Any

import httpx

from app.config import Settings
from app.models import Message
from app.policy import SYSTEM_PROMPT


class YandexModelError(RuntimeError):
    pass


def build_messages(history: list[Message], user_message: str) -> list[dict[str, str]]:
    messages = [{"role": "system", "text": SYSTEM_PROMPT}]
    messages.extend({"role": item.role, "text": item.text} for item in history)
    messages.append({"role": "user", "text": user_message})
    return messages


async def complete(
    settings: Settings,
    history: list[Message],
    user_message: str,
) -> str:
    if not settings.yandex_api_key:
        raise YandexModelError("Не задан YANDEX_API_KEY")
    if not settings.yandex_folder_id:
        raise YandexModelError("Не задан YANDEX_FOLDER_ID")

    payload: dict[str, Any] = {
        "modelUri": settings.yandex_model_uri,
        "completionOptions": {
            "stream": False,
            "temperature": 0.2,
            "maxTokens": 1200,
        },
        "messages": build_messages(history, user_message),
    }
    headers = {
        "Authorization": f"Api-Key {settings.yandex_api_key}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
            response = await client.post(
                settings.yandex_api_url,
                headers=headers,
                json=payload,
            )
    except httpx.HTTPError as exc:
        raise YandexModelError("Не удалось связаться с Yandex Cloud") from exc

    if response.is_error:
        raise YandexModelError(f"Yandex Cloud вернул HTTP {response.status_code}")

    try:
        data = response.json()
        answer = data["result"]["alternatives"][0]["message"]["text"]
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise YandexModelError("Yandex Cloud вернул неожиданный ответ") from exc

    if not isinstance(answer, str) or not answer.strip():
        raise YandexModelError("Модель вернула пустой ответ")
    return answer.strip()
