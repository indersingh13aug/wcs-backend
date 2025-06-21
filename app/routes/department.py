from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentOut
from app.database import get_db

router = APIRouter()

# Create a new department
@router.post("/departments", response_model=DepartmentOut)
def create_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    existing = db.query(Department).filter(Department.name == department.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Department with this name already exists")
    new_department = Department(**department.dict())
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department

# Get all departments (paginated)
@router.get("/departments", response_model=list[DepartmentOut])
def get_departments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Department).offset(skip).limit(limit).all()

@router.put("/departments/{department_id}/activate")
def activate_department(department_id: int, db: Session = Depends(get_db)):
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    department.is_deleted = False
    db.commit()
    db.refresh(department)
    return {"message": "Department activated successfully", "department": department}

@router.put("/departments/{department_id}/deactivate")
def deactivate_department(department_id: int, db: Session = Depends(get_db)):
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    department.is_deleted = True
    db.commit()
    db.refresh(department)
    return {"message": "Department deactivated successfully", "department": department}


# Get single department
@router.get("/departments/{department_id}", response_model=DepartmentOut)
def get_department(department_id: int, db: Session = Depends(get_db)):
    department = db.query(Department).filter(Department.id == department_id, Department.is_deleted == False).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@router.put("/departments/{department_id}", response_model=DepartmentOut)
def update_department(department_id: int, updated: DepartmentCreate, db: Session = Depends(get_db)):
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    # Check for duplicate name (excluding the current department)
    duplicate = db.query(Department).filter(
        Department.name == updated.name,
        Department.id != department_id
    ).first()
    if duplicate:
        raise HTTPException(status_code=400, detail="Department with this name already exists")

    # Update fields
    for key, value in updated.dict().items():
        setattr(department, key, value)

    db.commit()
    db.refresh(department)
    return department

# Soft delete department
@router.delete("/departments/{department_id}")
def delete_department(department_id: int, db: Session = Depends(get_db)):
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    department.is_deleted = True
    db.commit()
    return {"message": "Department soft-deleted successfully"}
