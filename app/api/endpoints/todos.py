from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db.models import Todo
from app.api.schemas import TodoCreate, TodoUpdate
from app.api.deps import get_db, get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/todos")
def create_todo(todo_data: TodoCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    todo = Todo(**todo_data.dict(), owner_id=user.id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@router.get("/todos")
def list_todos(db: Session = Depends(get_db), user=Depends(get_current_user)):
    todos = db.exec(select(Todo).where(Todo.owner_id == user.id)).all()
    now = datetime.utcnow()
    return {
        "completed": [t for t in todos if t.completed],
        "to_be_done": [t for t in todos if not t.completed and t.deadline > now],
        "time_elapsed": [t for t in todos if not t.completed and t.deadline <= now],
    }

@router.patch("/todos/{todo_id}/complete")
def mark_complete(todo_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    todo = db.get(Todo, todo_id)
    if not todo or todo.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.completed = True
    db.add(todo)
    db.commit()
    return {"message": "Todo marked as complete"}

@router.put("/todos/{todo_id}")
def update_todo(todo_id: int, updates: TodoUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    todo = db.get(Todo, todo_id)
    if not todo or todo.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(todo, field, value)
    db.commit()
    return todo

@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    todo = db.get(Todo, todo_id)
    if not todo or todo.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted"}
