from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.models.employee import Employee
from typing import Optional
from app.database import get_db
from app.models.role_user_map import RoleUserMap
from app.schemas.role_user_map import RoleUserAssign
from app.models.employee import Employee
from sqlalchemy import or_

router = APIRouter()

@router.get("/role-user/employees")
def get_employees_with_selected_or_no_role(
    selected_role: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    if selected_role is None:
        return []

    employees = db.query(Employee).filter(
        or_(
            Employee.role_id == None,
            Employee.role_id == selected_role
        )
    ).all()

    result = []
    for emp in employees:
        result.append({
            "id": emp.id,
            "full_name": f"{emp.first_name} {emp.last_name}",
            "role_id": emp.role_id,
            "is_selected": emp.role_id == selected_role
        })

    return result


@router.get("/role-user/assigned/{role_id}")
def get_assigned_employee_ids(role_id: int, db: Session = Depends(get_db)):
    mappings = db.query(RoleUserMap).filter(RoleUserMap.role_id == role_id).all()
    return [m.employee_id for m in mappings]



@router.put("/role-user/assign")
def assign_employees_to_role(data: RoleUserAssign, db: Session = Depends(get_db)):
    # Step 1: Clear role_id from employees who currently have this role
    db.query(Employee).filter(Employee.role_id == data.role_id).update(
        {Employee.role_id: None}, synchronize_session=False
    )

    # Step 2: Assign the role to selected employees
    if data.employee_ids:
        db.query(Employee).filter(Employee.id.in_(data.employee_ids)).update(
            {Employee.role_id: data.role_id}, synchronize_session=False
        )

    db.commit()
    return {"message": "Employees assigned to role successfully"}
