# app/routes/project.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectOut
from app.crud import project as crud
from app.database import get_db

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.project import Project
from app.models.client import Client
from app.models.employee import Employee
from app.schemas.project import ProjectOut

router = APIRouter()

@router.get("/projects", response_model=List[ProjectOut])
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()

    # Create mapping dictionaries
    client_map = {c.id: c.name for c in db.query(Client).all()}
    employee_map = {
        e.id: f"{e.first_name} {e.middle_name or ''} {e.last_name}".strip()
        for e in db.query(Employee).all()
    }
    print(employee_map)
    result = []

    for p in projects:
        # Parse assigned_team string -> List[int]
        assigned_ids = [int(emp_id) for emp_id in (p.assigned_team or "").split(",") if emp_id.strip().isdigit()]
        print(assigned_ids)
        # Lookup names
        # assigned_names = [employee_map.get(emp_id, "") for emp_id in assigned_ids]
        # assigned_names_str = ", ".join(name for name in assigned_names if name)
        assigned_names = [employee_map[i] for i in assigned_ids if i in employee_map]
        assigned_names_str = ", ".join(assigned_names)

        # Create enriched output
        out = ProjectOut.model_validate(p).model_copy(update={
            "client_name": client_map.get(p.client_id, ""),
            "assigned_team_names": assigned_names_str
        })
        result.append(out)

    return result


# @router.get("/projects", response_model=List[ProjectOut])
# def get_projects(include_deleted: bool = Query(False), db: Session = Depends(get_db)):
#     projects = crud.get_all_projects(db)
#     if not include_deleted:
#         projects = [p for p in projects if not p.is_deleted]
#     return projects

@router.post("/projects", response_model=ProjectOut)
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db, data)

@router.put("/projects/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, data: ProjectUpdate, db: Session = Depends(get_db)):
    updated = crud.update_project(db, project_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated

@router.put("/projects/{project_id}/deactivate", response_model=ProjectOut)
def deactivate(project_id: int, db: Session = Depends(get_db)):
    return crud.deactivate_project(db, project_id)

@router.put("/projects/{project_id}/activate", response_model=ProjectOut)
def activate(project_id: int, db: Session = Depends(get_db)):
    return crud.activate_project(db, project_id)
