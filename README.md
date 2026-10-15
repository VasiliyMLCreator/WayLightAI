# WayLight Medical Agent

Сервис принимает сообщение пользователя и историю переписки, передает их в Yandex Cloud Foundation Models и возвращает безопасный медицинский информационный ответ.

## Запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

В `.env` укажите `YANDEX_API_KEY` и `YANDEX_FOLDER_ID`. Шаблон использует `yandexgpt/latest`. Если в вашем каталоге Yandex Cloud доступна другая модель, укажите ее полный URI в `YANDEX_MODEL_URI`.

```bash
uvicorn app.main:app --reload
```

## Запрос

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"У меня болит горло второй день","history":[]}'
```

Поле `history` содержит элементы с ролями `user` и `assistant`. Ключ из `.env` не возвращается API и не должен коммититься.
