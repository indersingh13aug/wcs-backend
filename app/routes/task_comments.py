# app/routers/task_comments.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.task_comment import TaskComment
from app.models.employee import Employee
from app.schemas.task_assignment import TaskCommentCreate, TaskCommentOut
from datetime import datetime

router = APIRouter()


# @router.get("/task-assignments/{assignment_id}/comments", response_model=list[TaskCommentOut])
# def get_comments(assignment_id: int, db: Session = Depends(get_db)):
#     comments = db.query(TaskComment).filter(TaskComment.assignment_id == assignment_id).order_by(TaskComment.timestamp).all()
#     return [
#         TaskCommentOut(
#             id=c.id,
#             comment=c.comment,
#             timestamp=c.timestamp,
#             employee_name=f"{c.employee.first_name} {c.employee.last_name}",
#             status="New",
#         )
#         for c in comments
#     ]


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

@router.post("/task-comments", response_model=TaskCommentOut)
def create_comment(comment: TaskCommentCreate, db: Session = Depends(get_db)):
    db_comment = TaskComment(
        assignment_id=comment.assignment_id,
        employee_id=comment.employee_id,
        comment=comment.comment,
        timestamp=datetime.utcnow(),
        status=comment.status,
        assigned_to_id=comment.assigned_to_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    employee = db.query(Employee).filter(Employee.id == db_comment.employee_id).first()
    assigned_to = db.query(Employee).filter(Employee.id == db_comment.assigned_to_id).first()

    return {
        "id": db_comment.id,
        "comment": db_comment.comment,
        "timestamp": db_comment.timestamp,
        "employee_name": f"{employee.first_name} {employee.last_name}" if employee else "Unknown",
        "status": db_comment.status,
        "assigned_to": f"{assigned_to.first_name} {assigned_to.last_name}" if assigned_to else "Unknown"
    }

