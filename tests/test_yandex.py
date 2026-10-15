from app.models import Message
from app.yandex import build_messages


def test_build_messages_preserves_history_and_current_message() -> None:
    messages = build_messages(
        [Message(role="user", text="У меня температура")],
        "Что делать?",
    )
    assert messages[0]["role"] == "system"
    assert messages[-2:] == [
        {"role": "user", "text": "У меня температура"},
        {"role": "user", "text": "Что делать?"},
    ]
