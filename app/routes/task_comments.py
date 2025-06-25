# app/routers/task_comments.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.task_comment import TaskComment
from app.models.employee import Employee
from app.schemas.task_assignment import TaskCommentCreate, TaskCommentOut
from datetime import datetime

router = APIRouter()


@router.get("/task-assignments/{assignment_id}/comments", response_model=list[TaskCommentOut])
def get_comments(assignment_id: int, db: Session = Depends(get_db)):
    comments = db.query(TaskComment).filter(TaskComment.assignment_id == assignment_id).order_by(TaskComment.timestamp).all()
    return [
        TaskCommentOut(
            id=c.id,
            comment=c.comment,
            timestamp=c.timestamp,
            employee_name=f"{c.employee.first_name} {c.employee.last_name}"
        )
        for c in comments
    ]


@router.get("/task-comments/{assignment_id}", response_model=list[TaskCommentOut])
def get_comments_for_assignment(assignment_id: int, db: Session = Depends(get_db)):
    comments = db.query(TaskComment).filter_by(assignment_id=assignment_id).order_by(TaskComment.timestamp.desc()).all()
    result = []
    for c in comments:
        employee = db.query(Employee).filter_by(id=c.employee_id).first()
        result.append({
            **c.__dict__,
            "employee_name": f"{employee.first_name} {employee.last_name}" if employee else "Unknown"
        })
    return result

@router.post("/task-comments")
def add_comment(comment_data: TaskCommentCreate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter_by(id=comment_data.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    comment = TaskComment(
        assignment_id=comment_data.assignment_id,
        employee_id=comment_data.employee_id,
        comment=comment_data.comment
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)

    return {
        **comment.__dict__,
        "employee_name": f"{employee.first_name} {employee.last_name}"
    }
