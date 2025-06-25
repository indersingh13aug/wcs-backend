# routes/project_employee_map.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.project import Project
from app.models.employee import Employee
from app.models.project_employee_map import ProjectEmployeeMap
from typing import List
from app.schemas.project_employee_map import ProjectEmployeeMapOut,ProjectEmployeeMapCreate,ProjectEmployeeMapUpdate
from sqlalchemy.orm import joinedload
from collections import defaultdict
from datetime import datetime
from datetime import date

router = APIRouter()


@router.get("/project-employee-maps", response_model=List[ProjectEmployeeMapOut])
def get_all_mappings(db: Session = Depends(get_db)):
    mappings = (
        db.query(ProjectEmployeeMap)
        .options(
            joinedload(ProjectEmployeeMap.project),
            joinedload(ProjectEmployeeMap.employee).joinedload(Employee.role)
        )
        .all()
    )
    result = []
    for map in mappings:
        result.append({
            "id": map.id,
            "project": {
                "id": map.project.id,
                "name": map.project.name
            },
            "employee": {
                "id": map.employee.id,
                "first_name": map.employee.first_name,
                "last_name": map.employee.last_name,
                "role": {
                    "name": map.employee.role.name if map.employee.role else None
                },
                "ro_name": get_ro_name(db, map.employee.ro_id)
            },
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
def create_project_employee_map(
    payload: ProjectEmployeeMapCreate,
    db: Session = Depends(get_db)
):
    for emp_id in payload.employee_ids:
        mapping = ProjectEmployeeMap(
            project_id=payload.project_id,
            employee_id=emp_id,
            from_date=payload.from_date,
            to_date=payload.to_date,
            remarks=payload.remarks
        )
        db.add(mapping)
    db.commit()
    return {"message": "Project employee mappings created successfully"}

@router.put("/project-employee-maps/{id}/toggle-status")
def toggle_project_employee_map(id: int, db: Session = Depends(get_db)):
    record = db.query(ProjectEmployeeMap).filter(ProjectEmployeeMap.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Mapping not found")

    # If activating (is_deleted → False), check for existing duplicate
    if record.is_deleted:
        duplicate = db.query(ProjectEmployeeMap).filter(
            ProjectEmployeeMap.project_id == record.project_id,
            ProjectEmployeeMap.employee_id == record.employee_id,
            ProjectEmployeeMap.from_date == record.from_date,
            ProjectEmployeeMap.to_date == record.to_date,
            # ProjectEmployeeMap.remarks == record.remarks,
            ProjectEmployeeMap.is_deleted == False,
            ProjectEmployeeMap.id != record.id
        ).first()

        if duplicate:
            raise HTTPException(status_code=400, detail="Duplicate active mapping exists for this employee and project")

        record.is_deleted = False  # Activate

    else:
        record.is_deleted = True  # Deactivate

    db.commit()
    return {"message": "Status updated successfully"}



# @router.put("/project-employee-maps/{map_id}")
# def update_project_employee_map(map_id: int, data: ProjectEmployeeMapUpdate, db: Session = Depends(get_db)):
#     # 1. Check for duplicates
#     for emp_id in data.employee_ids:
#         duplicate = db.query(ProjectEmployeeMap).filter(
#             ProjectEmployeeMap.project_id == data.project_id,
#             ProjectEmployeeMap.employee_id == emp_id,
#             ProjectEmployeeMap.from_date == data.from_date,
#             ProjectEmployeeMap.to_date == data.to_date,
#             ProjectEmployeeMap.is_deleted == False,
#             ProjectEmployeeMap.id != map_id  # Don't compare with same group
#         ).first()
#         if duplicate:
#             raise HTTPException(status_code=409, detail=f"Mapping for Employee ID {emp_id} already exists.")

#     # 2. Delete all records with the same group map_id
#     existing_maps = db.query(ProjectEmployeeMap).filter(ProjectEmployeeMap.id == map_id).all()
#     for entry in existing_maps:
#         db.delete(entry)
#     db.commit()

#     # 3. Insert new entries
#     for emp_id in data.employee_ids:
#         new_map = ProjectEmployeeMap(
#             project_id=data.project_id,
#             employee_id=emp_id,
#             # from_date=datetime.strptime(data.from_date, "%Y-%m-%d").date(),
#             # to_date=datetime.strptime(data.to_date, "%Y-%m-%d").date(),
#             from_date = data.from_date if isinstance(data.from_date, date) else datetime.strptime(data.from_date, "%Y-%m-%d").date(),
#             to_date = data.to_date if isinstance(data.to_date, date) else datetime.strptime(data.to_date, "%Y-%m-%d").date(),

#             remarks=data.remarks,
#             # id=map_id,  # Reuse the same map_id for grouping
#             is_deleted=False
#         )
#         db.add(new_map)

#     db.commit()
#     return {"message": "Mapping updated successfully"}

@router.put("/project-employee-maps/{map_id}")
def update_mapping(map_id: int, data: ProjectEmployeeMapUpdate, db: Session = Depends(get_db)):
    # Step 1: Fetch the reference record from the ID passed
    base_record = db.query(ProjectEmployeeMap).filter(ProjectEmployeeMap.id == map_id).first()

    if not base_record:
        raise HTTPException(status_code=404, detail="Mapping not found")

    # Step 2: Find all records with same group info (matching project_id, from_date, to_date, remarks)
    related_mappings = db.query(ProjectEmployeeMap).filter(
        ProjectEmployeeMap.project_id == base_record.project_id,
        ProjectEmployeeMap.from_date == base_record.from_date,
        ProjectEmployeeMap.to_date == base_record.to_date,
        ProjectEmployeeMap.remarks == base_record.remarks
    ).all()

    related_ids = [rec.id for rec in related_mappings]
    old_emp_ids = [rec.employee_id for rec in related_mappings]

    # Step 3: Check duplicates before delete
    for emp_id in data.employee_ids:
        duplicate = db.query(ProjectEmployeeMap).filter(
            ProjectEmployeeMap.project_id == data.project_id,
            ProjectEmployeeMap.employee_id == emp_id,
            ProjectEmployeeMap.from_date == data.from_date,
            ProjectEmployeeMap.to_date == data.to_date,
            ProjectEmployeeMap.id.notin_(related_ids)  # exclude current editing group
        ).first()
        if duplicate:
            raise HTTPException(status_code=400, detail=f"Employee ID {emp_id} already mapped to the same project during this period.")

    # Step 4: Delete all records of that group
    for record in related_mappings:
        db.delete(record)
    db.commit()

    # Step 5: Insert new records
    new_records = [
        ProjectEmployeeMap(
            project_id=data.project_id,
            employee_id=emp_id,
            # from_date=data.from_date,
            # to_date=data.to_date,
            from_date = data.from_date if isinstance(data.from_date, date) else datetime.strptime(data.from_date, "%Y-%m-%d").date(),
            to_date = data.to_date if isinstance(data.to_date, date) else datetime.strptime(data.to_date, "%Y-%m-%d").date(),

            remarks=data.remarks
        ) for emp_id in data.employee_ids
    ]
    db.add_all(new_records)
    db.commit()

    return {"message": "Project mapping updated successfully"}


@router.delete("/project-employee-maps/{id}")
def hard_delete_project_employee_map(id: int, db: Session = Depends(get_db)):
    records = db.query(ProjectEmployeeMap).filter(ProjectEmployeeMap.id == id).all()
    if not records:
        raise HTTPException(status_code=404, detail="Mapping not found")
    
    for record in records:
        db.delete(record)  # ✅ Correct: passing one mapped instance at a time
    db.commit()
    return {"message": "Mapping permanently deleted"}

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
