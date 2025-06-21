from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeOut
from app.database import get_db
from sqlalchemy.orm import joinedload
import logging
logger = logging.getLogger(__name__)


router = APIRouter()

# Create new employee
@router.post("/employees", response_model=EmployeeOut)
def create_employee(emp: EmployeeCreate, db: Session = Depends(get_db)):
    logger.info("Creating new employee...")
    existing = db.query(Employee).filter(Employee.email == emp.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Employee already exists")
    new_emp = Employee(**emp.dict())
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp


@router.get("/employees", response_model=list[EmployeeOut])
def get_employees(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    logger.info("Getting all employees...")
    employees = (
        db.query(Employee)
        .options(joinedload(Employee.role), joinedload(Employee.department))
        .filter(Employee.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .all()
    )

    results = []
    for emp in employees:
        results.append({
        "id": emp.id,
        "user_id": emp.user_id,
        "first_name": emp.first_name,
        "middle_name": emp.middle_name,
        "last_name": emp.last_name,
        "email": emp.email,
        "date_of_joining": emp.date_of_joining,
        "status": emp.status,
        "role_id": emp.role_id,
        "department_id": emp.department_id,
        "role": {
            "id": emp.role.id,
            "name": emp.role.name
        } if emp.role else None,
        "department": {
            "id": emp.department.id,
            "name": emp.department.name
        } if emp.department else None
    })
    return results




# Get a single employee by ID
@router.get("/employees/{emp_id}", response_model=EmployeeOut)
def get_employee(emp_id: int, db: Session = Depends(get_db)):
    logger.info("Getting employee...",emp_id)
    emp = db.query(Employee).options(
        joinedload(Employee.department),
        joinedload(Employee.role)
    ).filter(Employee.id == emp_id).first()
    
    if not emp: 
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

# Update an employee
@router.put("/employees/{emp_id}", response_model=EmployeeOut)
def update_employee(emp_id: int, updated: EmployeeCreate, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    for key, value in updated.dict().items():
        setattr(emp, key, value)
    db.commit()
    db.refresh(emp)
    return emp

# Soft delete (mark deleted) - optional enhancement
@router.delete("/employees/{emp_id}")
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    emp.is_deleted = True
    db.commit()
    return {"message": "Employee soft-deleted successfully"}

