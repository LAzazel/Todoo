# FastAPI TodoApp (Short Guide)

Simple learning project with FastAPI, JWT auth, role-based access (`user`/`admin`), todo CRUD, and Alembic migrations.

## Quick Start

Run from project root (`fastApiProject`):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn sqlalchemy alembic passlib[bcrypt] python-jose[cryptography] python-multipart pydantic email-validator pytest
```

## Run API

Use package path from the root folder:

```powershell
python -m uvicorn TodoApp.main:app --reload
```

- Health check: `http://127.0.0.1:8000/health_check`
- Docs: `http://127.0.0.1:8000/docs`

## Alembic Migrations

Current `TodoApp/alembic/env.py` imports `models` directly, so run Alembic from `TodoApp`:

```powershell
Set-Location .\TodoApp
alembic upgrade head
alembic current
```

Create migration:

```powershell
Set-Location .\TodoApp
alembic revision -m "your_message"
```

## Tests

Run from project root:

```powershell
python -m pytest TodoApp/test -q
```

## Common Issue

### `ModuleNotFoundError: No module named 'TodoApp'`

Usually happens when starting from `TodoApp` folder with `uvicorn main:app`.

Use this instead from root:

```powershell
python -m uvicorn TodoApp.main:app --reload
```

