from fastapi import APIRouter, Depends, HTTPException, Query,File,UploadFile
from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeOut
from app.database import get_db
from sqlalchemy.orm import joinedload
from app.models.department import Department
from app.models.user import User
from app.schemas.employee import UserEmployeeOut,ITEmployeeOut
from uuid import uuid4
from pathlib import Path
from app.models.employee import EmployeeImage
import os

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

UPLOAD_DIR = Path("uploads/employees")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


router = APIRouter()


@router.get("/employee_with_image/{employee_id}")
def employee_with_image(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).options(
        joinedload(Employee.role),
        joinedload(Employee.department),
        joinedload(Employee.images)
    ).filter(Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    latest_image = None
    if employee.images:
        # Get the latest image
        latest_image = sorted(employee.images, key=lambda x: x.uploaded_at, reverse=True)[0].image_path

    return {
        "id": employee.id,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "email": employee.email,
        "role": {"id": employee.role.id, "name": employee.role.name} if employee.role else None,
        "department": {"id": employee.department.id, "name": employee.department.name} if employee.department else None,
        "date_of_joining": employee.date_of_joining,
        "status": employee.status,
        "image_path": latest_image,  # ⬅️ Add this
    }

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


@router.post("/employees/{employee_id}/upload-image")
async def upload_image(employee_id: int, image: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save image
    ext = os.path.splitext(image.filename)[1]
    filename = f"{uuid4()}{ext}"
    filepath = UPLOAD_DIR / filename

    with open(filepath, "wb") as f:
        content = await image.read()
        f.write(content)

    # Store image metadata in DB
    db_image = EmployeeImage(employee_id=employee_id, image_path=str(filepath))
    db.add(db_image)
    db.commit()

    return {"message": "Image uploaded", "filename": filename}

def get_ro_name(db: Session, ro_id: int) -> str:
    if not ro_id:
        return ""

    ro = db.query(Employee).filter(Employee.id == ro_id, Employee.is_deleted == False).first()
    if ro:
        return f"{ro.first_name} {ro.last_name}"
    return "Unknown"

@router.get("/employees", response_model=list[EmployeeOut])
def get_employees(skip: int = 0, limit: int = 5,db: Session = Depends(get_db)):
    employees = db.query(Employee)\
        .options(joinedload(Employee.role), joinedload(Employee.department))\
        .filter(Employee.is_deleted == False)\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    result = []

    for e in employees:
        result.append({
            "id": e.id,
            "user_id": e.user_id,
            "first_name": e.first_name,
            "middle_name": e.middle_name,
            "last_name": e.last_name,
            "email": e.email,
            "date_of_joining": e.date_of_joining,
            "status": e.status,
            "role": {"id": e.role.id, "name": e.role.name} if e.role else None,
            "department": {"id": e.department.id, "name": e.department.name} if e.department else None,
            "ro_name": get_ro_name(db, e.ro_id)
        })

    return result


# @router.get("/employees/availableforuser", response_model=list[ITEmployeeOut])
# def get_available_employees_for_user(db: Session = Depends(get_db)):
#     # Get employee_ids that already have a user
#     used_employee_ids = db.query(User.employee_id).all()
#     used_employee_ids = [id for (id,) in used_employee_ids]  # unpack tuples

#     # Fetch active employees who do not have users
#     employees = (
#         db.query(Employee)
#         .filter(
#             Employee.status == "Active",
#             ~Employee.id.in_(used_employee_ids)
#         )
#         .all()
#     )

#     result = [
#         ITEmployeeOut(
#             id=emp.id,
#             full_name=" ".join(
#                 filter(None, [emp.first_name, emp.middle_name, emp.last_name])
#             ).strip()
#         )
#         for emp in employees
#     ]

#     return result

# @router.get("/employees/availableforuser", response_model=list[UserEmployeeOut])
# def get_available_employees_for_user(role_id: int = Query(...), db: Session = Depends(get_db)):
#     used_employee_ids = db.query(User.employee_id).all()
#     used_employee_ids = [id for (id,) in used_employee_ids]

#     employees = (
#         db.query(Employee)
#         .filter(
#             Employee.status == "Active",
#             ~Employee.id.in_(used_employee_ids)
#         )
#         .all()
#     )

#     result = [
#         ITEmployeeOut(
#             id=emp.id,
#             first_name=emp.first_name,
#             last_name=emp.last_name,
#             full_name=" ".join(filter(None, [emp.first_name, emp.middle_name, emp.last_name])).strip()
#         )
#         for emp in employees
#     ]

#     return result


@router.get("/employees/availableforuser", response_model=list[UserEmployeeOut])
def get_available_employees_for_user(role_id: int = Query(...), db: Session = Depends(get_db)):
    # Get employee_ids that already have a user
    used_employee_ids = db.query(User.employee_id).filter(User.is_deleted == False).all()
    used_employee_ids = [id for (id,) in used_employee_ids]  # unpack tuples

    # Fetch active employees who match the role and have no user
    employees = (
        db.query(Employee)
        .filter(
            Employee.status == "Active",
            Employee.role_id == role_id,
            ~Employee.id.in_(used_employee_ids),
            Employee.is_deleted == False
        )
        .all()
    )

    result = [
        UserEmployeeOut(
            id=emp.id,
            full_name=" ".join(
                filter(None, [emp.first_name, emp.middle_name, emp.last_name])
            ).strip()
        )
        for emp in employees
    ]

    return result

# Get a single employee by ID
@router.get("/employees/{emp_id}", response_model=EmployeeOut)
def get_employee(emp_id: int, db: Session = Depends(get_db)):
    logger.info(f"Getting employee... {emp_id}")
    
    emp = db.query(Employee).options(
        joinedload(Employee.department),
        joinedload(Employee.role)
    ).filter(Employee.id == emp_id).first()
    
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return emp  # ✅ You forgot this line


@router.get("/it", response_model=list[ITEmployeeOut])
def get_it_employees(db: Session = Depends(get_db)):
    employees = (
        db.query(Employee)
        .join(Department, Employee.department_id == Department.id)
        .filter(Department.name == "IT", Employee.status == "Active")
        .all()
    )

    result = [ITEmployeeOut.model_validate(emp) for emp in employees]
    return result


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

