# Todoo

REST API для управління особистими задачами (todo-list). Побудований на FastAPI з JWT-автентифікацією та SQLite.

## Стек

- **Python 3.11+**
- **FastAPI** — веб-фреймворк
- **SQLAlchemy** — ORM
- **SQLite** — база даних
- **JWT** — автентифікація
- **pytest** — тестування

## Структура проекту

```
Todoo/
├── app/
│   ├── domain/                        # Бізнес-логіка. Не імпортує нічого зовнішнього
│   │   ├── models/
│   │   │   ├── user.py                # Доменна модель User
│   │   │   └── todo.py                # Доменна модель Todo
│   │   ├── value_objects/
│   │   │   ├── email.py               # Email з валідацією формату
│   │   │   └── priority.py            # Priority (1–5)
│   │   ├── repositories/
│   │   │   ├── user_repo.py           # Інтерфейс IUserRepository (ABC)
│   │   │   └── todo_repo.py           # Інтерфейс ITodoRepository (ABC)
│   │   ├── factories/
│   │   │   ├── user_factory.py        # Створення User з перевіркою унікальності
│   │   │   └── todo_factory.py        # Створення Todo з перевіркою інваріантів
│   │   └── errors.py                  # Доменні помилки (без HTTP)
│   │
│   ├── application/
│   │   ├── commands/                      # Змінюють стан, не повертають дані
│   │   │   ├── todos/
│   │   │   │   ├── create_todo.py         # sync: audit напряму
│   │   │   │   ├── delete_todo.py         # sync: audit напряму
│   │   │   │   ├── change_status.py       # sync: audit напряму
│   │   │   │   └── update_todo.py         # async: publish TodoUpdated
│   │   │   ├── users/
│   │   │   │   ├── register_user.py       # sync: audit напряму
│   │   │   │   ├── change_password.py     # async: publish UserPasswordChanged
│   │   │   │   └── change_phone.py        # async: publish UserPhoneChanged
│   │   │   └── admin/
│   │   │       └── delete_user.py         # async: publish UserDeleted
│   │   │
│   │   ├── queries/                   # Читають стан, повертають Read Models
│   │   │   ├── todos/
│   │   │   │   ├── get_todo.py        # GetTodoQuery + Handler → TodoReadModel
│   │   │   │   └── get_all_todos.py   # GetAllTodosQuery + Handler → List[TodoReadModel]
│   │   │   ├── users/
│   │   │   │   └── get_profile.py     # GetProfileQuery + Handler → UserReadModel
│   │   │   ├── admin/
│   │   │   │   └── get_all_users.py   # GetAllUsersQuery + Handler → List[UserReadModel]
│   │   │   └── auth/
│   │   │       └── login.py           # LoginQuery + Handler → JWT token
│   │   │
│   │   ├── events/                        # Доменні події (frozen dataclasses)
│   │   │   ├── base.py                    # DomainEvent
│   │   │   ├── todo_events.py             # TodoUpdated
│   │   │   └── user_events.py             # UserPasswordChanged, UserPhoneChanged, UserDeleted
│   │   │
│   │   ├── read_models/               # DTO оптимізовані під відповідь клієнту
│   │   │   ├── todo_read_model.py     # TodoReadModel (frozen dataclass)
│   │   │   └── user_read_model.py     # UserReadModel (frozen dataclass)
│   │   │
│   │   └── interfaces/
│   │       └── auth_services.py       # IPasswordHasher, ITokenService
│   │
│   ├── infrastructure/                # Реалізації. Залежить від domain
│   │   ├── orm/
│   │   │   └── models.py              # SQLAlchemy ORM-моделі (UserORM, TodoORM)
│   │   ├── repositories/
│   │   │   ├── user_repo.py           # SQLAlchemyUserRepository
│   │   │   └── todo_repo.py           # SQLAlchemyTodoRepository
│   │   ├── mappers/
│   │   │   ├── user_mapper.py         # UserORM ↔ User
│   │   │   └── todo_mapper.py         # TodoORM ↔ Todo
│   │   ├── auth/
│   │   │   └── jwt_service.py         # PasslibPasswordHasher, JoseTokenService
│   │   ├── audit/                         # Допоміжний компонент
│   │   │   ├── audit_log.py               # AuditLog dataclass
│   │   │   ├── interfaces.py              # IAuditService (ABC)
│   │   │   ├── audit_service.py           # InMemoryAuditService
│   │   │   └── subscribers.py             # Підписники для async варіанту
│   │   └── event_bus/
│   │   │   ├── interfaces.py              # IEventBus (ABC)
│   │   │   └── in_memory_bus.py           # InMemoryEventBus
│   │   └── database.py                # SQLAlchemy engine, session, get_db
│   │
│   ├── presentation/                  # HTTP шар. Залежить від application
│   │   ├── routers/
│   │   │   ├── auth.py                # POST /auth/register, POST /auth/login
│   │   │   ├── todos.py               # CRUD /todos/
│   │   │   ├── users.py               # GET/PUT /user/
│   │   │   └── admin.py               # GET/DELETE /admin/users
│   │   ├── dependencies.py            # FastAPI Depends()
│   │   └── error_handler.py           # DomainError → HTTP статус
│   │
│   ├── config.py                      # Змінні середовища
│   └── main.py                        # Точка входу FastAPI
│
├── tests/
│   ├── unit/
│   │   ├── domain/
│   │   │   ├── test_value_objects.py  # Email, Priority
│   │   │   ├── test_models.py         # User, Todo — поведінка та інваріанти
│   │   │   └── test_factories.py      # UserFactory, TodoFactory
│   │   └── application/
│   │       ├── test_commands.py       # Command Handlers без БД
│   │       └── test_communication.py  # TestSyncAsyncCommunication
│   └── integration/
│       └── test_api.py                # HTTP → реальна тестова БД
│
├── docs/
│   ├── use-cases.md
│   └── analysis/
│       ├── lab2.md
│       ├── lab3.md
│       └── lab4.md
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## Правило залежностей
 
```
Presentation → Commands/Queries → Domain ← Infrastructure
```

## Архітектура комунікації
 
```
Sync:  Handler -> IAuditService.log()
Async: Handler -> IEventBus.publish(Event) -> Subscriber -> IAuditService.log()
```
 
**Sync хендлери** (create, delete, change_status, register): викликають аудит напряму, збій аудиту ігнорується через `try/except`.
 
**Async хендлери** (update, change_password, change_phone, delete_user): публікують подію і одразу повертають результат, підписники обробляють незалежно.

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

Документація API: [http://localhost:8000/docs](http://localhost:8000/docs)

## API
 
| Метод | Ендпоінт | Тип | Комунікація | Авторизація |
|---|---|---|---|---|
| POST | `/auth/register` | Command | sync | — |
| POST | `/auth/login` | Query | — | — |
| GET | `/todos/` | Query | — | ✅ |
| POST | `/todos/` | Command | sync | ✅ |
| GET | `/todos/{id}` | Query | — | ✅ |
| PUT | `/todos/{id}` | Command | async | ✅ |
| DELETE | `/todos/{id}` | Command | sync | ✅ |
| PATCH | `/todos/{id}/status` | Command | sync | ✅ |
| GET | `/user/` | Query | — | ✅ |
| PUT | `/user/change_password` | Command | async | ✅ |
| PUT | `/user/change_phone_number` | Command | async | ✅ |
| GET | `/admin/users` | Query | — | ✅ admin |
| DELETE | `/admin/users/{id}` | Command | async | ✅ admin |


## Тестування
 
```bash
pytest
```
 
Тільки unit-тести (без БД):
 
```bash
pytest tests/unit/ -v
```

Тести комунікації sync/async:
```bash
pytest tests/unit/application/test_communication.py -v
```
 
Тільки інтеграційні тести:
 
```bash
pytest tests/integration/ -v
```
