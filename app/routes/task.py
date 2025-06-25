from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from typing import List

router = APIRouter()

@router.get("/tasks", response_model=List[TaskOut])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@router.post("/tasks", response_model=TaskOut)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    task = Task(**data.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in data.dict().items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

@router.put("/tasks/{task_id}/deactivate")
def deactivate_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.is_deleted = True
    db.commit()
    return {"message": "Task deactivated"}

@router.put("/tasks/{task_id}/activate")
def activate_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.is_deleted = False
    db.commit()
    return {"message": "Task activated"}
