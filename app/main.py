from fastapi import FastAPI, HTTPException

from app.config import get_settings
from app.models import ChatRequest, ChatResponse
from app.policy import is_emergency
from app.yandex import YandexModelError, complete

app = FastAPI(title="WayLight Medical Agent", version="1.0.0")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    settings = get_settings()
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=422, detail="Сообщение не должно быть пустым")
    if len(message) > settings.max_message_length:
        raise HTTPException(
            status_code=422,
            detail=f"Сообщение не должно превышать {settings.max_message_length} символов",
        )

    history = [
        item.model_copy(update={"text": item.text[: settings.max_message_length]})
        for item in request.history[-settings.max_history_messages :]
    ]
    emergency = is_emergency(message)
    try:
        answer = await complete(settings, history, message)
    except YandexModelError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return ChatResponse(answer=answer, emergency=emergency)
