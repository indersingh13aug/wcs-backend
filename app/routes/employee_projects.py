# routers/employee_projects.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.task_assignment import TaskAssignment
from app.models.project import Project
from app.models.employee import Employee
from app.database import get_db

router = APIRouter()

@router.get("/employee/{employee_id}/active-projects")
def get_active_projects_for_employee(employee_id: int, db: Session = Depends(get_db)):
    assignments = (
        db.query(TaskAssignment)
        .filter(TaskAssignment.employee_id == employee_id, TaskAssignment.status != "Close")
        .all()
    )
    project_ids = list({a.project_id for a in assignments})
    projects = db.query(Project).filter(Project.id.in_(project_ids)).all()

    return [
        {
            "project_id": p.id,
            "project_name": p.name,
        }
        for p in projects
    ]


@router.get("/employee/{employee_id}/project-tasks/{project_id}")
def get_project_tasks_for_employee(employee_id: int, project_id: int, db: Session = Depends(get_db)):
    assignments = (
        db.query(TaskAssignment)
        .filter(
            TaskAssignment.employee_id == employee_id,
            TaskAssignment.project_id == project_id,
            TaskAssignment.status != "Close"
        )
        .all()
    )

    return [
        {
            "assignment_id": a.id,
            "task_id": a.task_id,
            "task_name": a.task.name
        }
        for a in assignments
    ]
