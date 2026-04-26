# ToDo List MVP

## Запуск

```bash
# Установить зависимости
pip install fastapi uvicorn

# Запустить
python server.py
```

Откроется http://localhost:3000

## Структура

- `frontend/` — HTML, CSS, JS
- `backend/data/tasks.json` — задачи
- `server.py` — единый сервер (фронт + API)

## API

- `GET /api/tasks?view=active` — активные
- `GET /api/tasks?view=done` — выполненные
- `GET /api/tasks?view=trash` — корзина
- `POST /api/tasks` — добавить
- `PATCH /api/tasks/:id` — обновить
- `DELETE /api/tasks/:id` — в корзину
- `POST /api/tasks/:id/restore` — восстановить
- `DELETE /api/tasks/:id/permanent` — удалить