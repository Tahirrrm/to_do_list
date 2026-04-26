# ToDo List MVP

Чистый Python (без фреймворков).

## Запуск

```bash
python server.py
```

Откроется http://localhost:3000

## Структура

```
to_do_list/
├── frontend/
│   ├── index.html
│   └── src/
│       ├── main.js
│       └── style.css
├── backend/data/
│   └── tasks.json
├── server.py      # чистый Python http.server
├── .gitignore
└── README.md
```

## API

- `GET /api/tasks?view=active` — активные
- `GET /api/tasks?view=done` — выполненные
- `GET /api/tasks?view=trash` — корзина
- `POST /api/tasks` — добавить `{"title": "..."}`
- `PATCH /api/tasks/:id` — обновить `{"status": "done"}`
- `DELETE /api/tasks/:id` — в корзину
- `POST /api/tasks/:id/restore` — восстановить
- `DELETE /api/tasks/:id/permanent` — удалить навсегда