from fastapi import Depends, HTTPException, Path, APIRouter
from typing import Annotated
from starlette import status
from ..models import Todos
from .auth import get_current_user
from ..dependencies import db_dependency


router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


user_dependency = Annotated[dict, Depends(get_current_user)]



@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo_model)
    db.commit()
    return None

