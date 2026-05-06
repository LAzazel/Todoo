# Todoo

REST API для управління особистими задачами (todo-list). Побудований на FastAPI з JWT-автентифікацією та SQLite.

## Стек

- **Python 3.11+**
- **FastAPI** — веб-фреймворк
- **SQLAlchemy** — ORM
- **SQLite** — база даних
- **JWT** — автентифікація
- **pytest + httpx** — тестування

## Структура проекту

```
Todoo/
├── app/
│   ├── auth.py          # JWT логіка, реєстрація, логін
│   ├── main.py          # точка входу FastAPI
│   ├── models.py        # моделі БД
│   ├── database.py      # підключення до БД
│   ├── dependencies.py  # спільні залежності
│   ├── config.py        # змінні середовища
│   └── routers/
│       ├── todos.py     # CRUD задач
│       ├── users.py     # профіль користувача
│       └── admin.py     # адмін-ендпоінти
├── tests/
│   ├── conftest.py           # фікстури
│   ├── test_auth_unit.py     # unit-тести
│   └── test_integration.py  # інтеграційні тести
├── docs/
│   └── use-cases.md
├── .env.example
└── requirements.txt
```

## Запуск

### 1. Клонувати репозиторій

```bash
git clone https://github.com/<your-username>/Todoo.git
cd Todoo
```

### 2. Створити віртуальне середовище та встановити залежності

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Налаштувати змінні середовища

```bash
cp .env.example .env
```

Відкрити `.env` і встановити `SECRET_KEY` — власний випадковий рядок:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Вставити результат у `.env`:

```
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```

### 4. Запустити сервер

```bash
uvicorn app.main:app --reload
```

API буде доступне за адресою: [http://localhost:8000](http://localhost:8000)

Документація: [http://localhost:8000/docs](http://localhost:8000/docs)

## API

| Метод | Ендпоінт | Опис | Авторизація |
|---|---|---|---|
| POST | `/auth/` | Реєстрація | — |
| POST | `/auth/token` | Вхід, отримання JWT | — |
| GET | `/todos/` | Список своїх задач | ✅ |
| POST | `/todos/` | Створити задачу | ✅ |
| GET | `/todos/{id}` | Отримати задачу | ✅ |
| PUT | `/todos/{id}` | Оновити задачу | ✅ |
| DELETE | `/todos/{id}` | Видалити задачу | ✅ |
| GET | `/user/` | Свій профіль | ✅ |
| PUT | `/user/change_password` | Змінити пароль | ✅ |
| PUT | `/user/change_phone_number` | Змінити телефон | ✅ |
| GET | `/admin/users` | Всі користувачі (адмін) | ✅ admin |
| DELETE | `/admin/users/{id}` | Видалити користувача (адмін) | ✅ admin |

## Тестування

```bash
pytest
```

Запустити тільки unit-тести:

```bash
pytest tests/test_auth_unit.py -v
```

Запустити тільки інтеграційні тести:

```bash
pytest tests/test_integration.py -v
```
