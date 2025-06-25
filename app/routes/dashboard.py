# app/routes/dashboard.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employee import Employee
from app.models.department import Department

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    employee_count = db.query(Employee).count()
    department_count = db.query(Department).count()


    return {
        "employees": employee_count,
        "departments": department_count,
    }
