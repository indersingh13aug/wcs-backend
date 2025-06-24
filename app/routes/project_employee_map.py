# routes/project_employee_map.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.project import Project
from app.models.employee import Employee
from app.models.project_employee_map import ProjectEmployeeMap
from typing import List
from app.schemas.project_employee_map import ProjectEmployeeMapOut,ProjectEmployeeMapCreate

router = APIRouter()


@router.get("/project-employee-maps", response_model=List[ProjectEmployeeMapOut])
def get_all_mappings(db: Session = Depends(get_db)):
    mappings = db.query(ProjectEmployeeMap).filter().all()
    result = []
    for map in mappings:
        result.append({
            "id": map.id,
            "project": {
                "id": map.project.id,
                "name": map.project.name
            },
            "employees": [{
                "id": e.id,
                "first_name": e.first_name,
                "last_name": e.last_name,
                "role": {"name": e.role.name if e.role else None},
                "ro_name": get_ro_name(db, e.ro_id)
            } for e in map.employees],
            "from_date": map.from_date,
            "to_date": map.to_date,
            "remarks": map.remarks,
            "is_deleted": map.is_deleted
        })
    return result

def get_ro_name(db: Session, ro_id: int):
    ro = db.query(Employee).filter_by(id=ro_id).first()
    return f"{ro.first_name} {ro.last_name}" if ro else "-"

@router.post("/project-employee-maps")
def create_project_employee_map(data: ProjectEmployeeMapCreate, db: Session = Depends(get_db)):
    created = []
    for emp_id in data.employee_ids:
        row = ProjectEmployeeMap(
            project_id=data.project_id,
            employee_id=emp_id,
            from_date=data.from_date,
            to_date=data.to_date,
            remarks=data.remarks,
            is_deleted=False
        )
        db.add(row)
        created.append(row)
    db.commit()
    return {"status": "success", "mapped_count": len(created)}


@router.put("/project-employee-maps/{map_id}")
def update_mapping(map_id: int, payload: ProjectEmployeeMapCreate, db: Session = Depends(get_db)):
    mapping = db.query(ProjectEmployeeMap).filter_by(id=map_id).first()
    if not mapping:
        raise HTTPException(status_code=404, detail="Mapping not found")
    
    mapping.project_id = payload.project_id
    mapping.from_date = payload.from_date
    mapping.to_date = payload.to_date
    mapping.remarks = payload.remarks
    mapping.employees = db.query(Employee).filter(Employee.id.in_(payload.employee_ids)).all()
    db.commit()
    return {"message": "Mapping updated successfully"}

@router.put("/project-employee-maps/{map_id}/activate")
def activate_mapping(map_id: int, db: Session = Depends(get_db)):
    mapping = db.query(ProjectEmployeeMap).filter_by(id=map_id).first()
    if not mapping:
        raise HTTPException(status_code=404, detail="Mapping not found")
    mapping.is_deleted = False
    db.commit()
    return {"message": "Mapping activated"}

@router.put("/project-employee-maps/{map_id}/deactivate")
def deactivate_mapping(map_id: int, db: Session = Depends(get_db)):
    mapping = db.query(ProjectEmployeeMap).filter_by(id=map_id).first()
    if not mapping:
        raise HTTPException(status_code=404, detail="Mapping not found")
    mapping.is_deleted = True
    db.commit()
    return {"message": "Mapping deactivated"}
