from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.task_assignment import TaskAssignment
from app.models.task_comment import TaskComment
from app.models.employee import Employee
from app.schemas.task_assignment import (
    TaskAssignmentCreate, TaskAssignmentOut,
    TaskCommentCreate, TaskCommentOut
)

router = APIRouter()

@router.post("/task-assignments", response_model=TaskAssignmentOut)
def create_assignment(data: TaskAssignmentCreate, db: Session = Depends(get_db)):
    assignment = TaskAssignment(**data.dict())
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

@router.get("/task-assignments", response_model=list[TaskAssignmentOut])
def list_assignments(db: Session = Depends(get_db)):
    
    return db.query(TaskAssignment).all()

@router.post("/task-assignments/comments", response_model=TaskCommentOut)
def add_comment(data: TaskCommentCreate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == data.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    comment = TaskComment(
        assignment_id=data.assignment_id,
        employee_id=data.employee_id,
        comment=data.comment
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)

    return TaskCommentOut(
        id=comment.id,
        comment=comment.comment,
        timestamp=comment.timestamp,
        employee_name=f"{employee.first_name} {employee.last_name}"
    )

@router.get("/task-assignments/{assignment_id}/comments", response_model=list[TaskCommentOut])
def get_comments(assignment_id: int, db: Session = Depends(get_db)):
    comments = db.query(TaskComment).filter(TaskComment.assignment_id == assignment_id).order_by(TaskComment.timestamp).all()
    return [
        TaskCommentOut(
            id=c.id,
            comment=c.comment,
            timestamp=c.timestamp,
            employee_name=f"{c.employee.first_name} {c.employee.last_name}"
        ) for c in comments
    ]
