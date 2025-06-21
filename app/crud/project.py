# app/crud/project.py
from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

def get_all_projects(db: Session):
    return db.query(Project).all()

def create_project(db: Session, data: ProjectCreate):
    new_project = Project(**data.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

def update_project(db: Session, project_id: int, data: ProjectUpdate):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return None
    for key, value in data.dict().items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project

def deactivate_project(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        project.is_deleted = True
        db.commit()
    return project

def activate_project(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        project.is_deleted = False
        db.commit()
    return project
