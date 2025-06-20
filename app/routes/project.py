from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.project import Project
from app.models.client import Client
from app.schemas.project import ProjectCreate, ProjectOut

router = APIRouter()

# Create new project
@router.post("/projects/", response_model=ProjectOut)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    # Validate client ID
    client = db.query(Client).filter(Client.id == project.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    new_project = Project(**project.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

# Get all projects
@router.get("/projects/", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()

# Get project by ID
@router.get("/projects/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# Update project
@router.put("/projects/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, updated: ProjectCreate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in updated.dict().items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project

# Delete project
@router.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.is_deleted = True
    db.commit()
    return {"message": "Project deleted successfully"}
