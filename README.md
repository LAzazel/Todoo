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
│   ├── application/                   # Use cases. Залежить тільки від domain
│   │   ├── use_cases/
│   │   │   ├── auth/
│   │   │   │   ├── register.py        # RegisterUserUseCase
│   │   │   │   └── login.py           # LoginUserUseCase
│   │   │   ├── todos/
│   │   │   │   ├── create.py          # CreateTodoUseCase
│   │   │   │   ├── get.py             # GetTodoUseCase, GetAllUserTodosUseCase
│   │   │   │   ├── update.py          # UpdateTodoUseCase
│   │   │   │   ├── delete.py          # DeleteTodoUseCase
│   │   │   │   └── status.py          # ChangeTodoStatusUseCase
│   │   │   ├── users/
│   │   │   │   └── profile.py         # GetUserProfileUseCase, ChangePasswordUseCase
│   │   │   └── admin/
│   │   │       ├── get_all.py         # AdminGetAllUsersUseCase
│   │   │       └── delete_user.py     # AdminDeleteUserUseCase
│   │   ├── dto/
│   │   │   ├── user_dto.py            # RegisterUserDTO, LoginUserDTO, UserResponseDTO
│   │   │   └── todo_dto.py            # CreateTodoDTO, UpdateTodoDTO, TodoResponseDTO
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
│   │       └── test_use_cases.py      # Всі use cases з fake-репозиторіями
│   └── integration/
│       └── test_api.py                # HTTP → реальна тестова БД
│
├── docs/
│   ├── use-cases.md
│   └── analysis/
│       └── lab2.md
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## Правило залежностей
 
```
Presentation → Application → Domain ← Infrastructure
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

Документація API: [http://localhost:8000/docs](http://localhost:8000/docs)

## API
 
| Метод | Ендпоінт | Опис | Авторизація |
|---|---|---|---|
| POST | `/auth/register` | Реєстрація | — |
| POST | `/auth/login` | Вхід, отримання JWT | — |
| GET | `/todos/` | Список своїх задач | ✅ |
| POST | `/todos/` | Створити задачу | ✅ |
| GET | `/todos/{id}` | Отримати задачу | ✅ |
| PUT | `/todos/{id}` | Оновити задачу | ✅ |
| DELETE | `/todos/{id}` | Видалити задачу | ✅ |
| PATCH | `/todos/{id}/status` | Змінити статус | ✅ |
| GET | `/user/` | Свій профіль | ✅ |
| PUT | `/user/change_password` | Змінити пароль | ✅ |
| PUT | `/user/change_phone_number` | Змінити телефон | ✅ |
| GET | `/admin/users` | Всі користувачі | ✅ admin |
| DELETE | `/admin/users/{id}` | Видалити користувача | ✅ admin |

## Тестування
 
```bash
pytest
```
 
Тільки unit-тести домену:
 
```bash
pytest tests/unit/domain/ -v
```
 
Тільки unit-тести application layer:
 
```bash
pytest tests/unit/application/ -v
```
 
Тільки інтеграційні тести:
 
```bash
pytest tests/integration/ -v
```
 