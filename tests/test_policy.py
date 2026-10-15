from app.policy import is_emergency


def test_detects_emergency_language() -> None:
    assert is_emergency("Мне трудно дышать и появилась боль в груди")


def test_does_not_flag_general_question() -> None:
    assert not is_emergency("Что такое сезонная аллергия?")
