from fastapi import FastAPI
from app.infrastructure.database import engine, Base

from app.presentation.routers import auth, todos, users, admin

from app.domain import errors
from app.presentation.error_handler import domain_error_exception_handler

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todoo API", description="A simple To-Do application with layered architecture", version="1.0.0")

app.add_exception_handler(errors.DomainError, domain_error_exception_handler)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "Welcome to Todoo API"}