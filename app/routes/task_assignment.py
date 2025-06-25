from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from app.database import get_db
from app.models.task_assignment import TaskAssignment
from app.models.task_comment import TaskComment
from app.models.employee import Employee
from app.models.project_employee_map import ProjectEmployeeMap

from app.schemas.task_assignment import (
    TaskAssignmentCreate, TaskAssignmentOut,
    TaskCommentCreate, TaskCommentOut
)
from app.schemas.employee import EmployeeTaskOut

router = APIRouter()

@router.get("/employees/{employee_id}/assignments", response_model=list[TaskAssignmentOut])
def get_assignments_for_employee(employee_id: int, db: Session = Depends(get_db)):
    assignments = db.query(TaskAssignment)\
        .options(
            joinedload(TaskAssignment.project),
            joinedload(TaskAssignment.task),
            joinedload(TaskAssignment.employee)
        )\
        .filter(TaskAssignment.employee_id == employee_id)\
        .all()

    return assignments


@router.get("/projects/{project_id}/employees", response_model=list[EmployeeTaskOut])
def get_employees_by_project(project_id: int, db: Session = Depends(get_db)):
    mappings = db.query(ProjectEmployeeMap).filter(
        ProjectEmployeeMap.project_id == project_id,
        ProjectEmployeeMap.is_deleted == False
    ).all()

    employee_ids = [m.employee_id for m in mappings]

    employees = db.query(Employee).filter(
        Employee.id.in_(employee_ids),
        Employee.is_deleted == False
    ).all()

    return employees

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


@router.get("/projects/{project_id}/employees")
def get_project_employees(project_id: int, db: Session = Depends(get_db)):
    employee_ids = (
        db.query(TaskAssignment.employee_id)
        .filter(TaskAssignment.project_id == project_id)
        .distinct()
        .all()
    )
    ids = [eid[0] for eid in employee_ids]
    employees = db.query(Employee).filter(Employee.id.in_(ids)).all()
    return [
        {"id": e.id, "first_name": e.first_name, "last_name": e.last_name}
        for e in employees
    ]


@router.put("/task-assignments/{assignment_id}")
def update_task_assignment(assignment_id: int, data: dict, db: Session = Depends(get_db)):
    assignment = db.query(TaskAssignment).filter_by(id=assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    assignment.status = data.get("status", assignment.status)
    assignment.employee_id = data.get("employee_id", assignment.employee_id)
    db.commit()
    return {"message": "Updated"}


@router.get("/task-assignments")
def get_assignment(project_id: int, task_id: int, employee_id: int, db: Session = Depends(get_db)):
    assignment = (
        db.query(TaskAssignment)
        .filter_by(project_id=project_id, task_id=task_id, employee_id=employee_id)
        .first()
    )
    if not assignment:
        return []

    return [{
        "id": assignment.id,
        "project_id": assignment.project_id,
        "task_id": assignment.task_id,
        "employee_id": assignment.employee_id,
        "start_date": assignment.start_date,
        "end_date": assignment.end_date,
        "status": assignment.status,
    }]


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
    comments = db.query(TaskComment).filter(TaskComment.assignment_id == assignment_id).order_by(TaskComment.timestamp.desc()).all()
    results = []

    for c in comments:
        employee = db.query(Employee).filter(Employee.id == c.employee_id).first()
        assigned_to = db.query(Employee).filter(Employee.id == c.assigned_to_id).first() if c.assigned_to_id else None

        results.append(TaskCommentOut(
            id=c.id,
            comment=c.comment,
            timestamp=c.timestamp,
            employee_name=f"{employee.first_name} {employee.last_name}" if employee else "Unknown",
            status=c.status,
            assigned_to=f"{assigned_to.first_name} {assigned_to.last_name}" if assigned_to else "N/A"
        ))

    return results

