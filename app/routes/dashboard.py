# app/routes/dashboard.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employee import Employee
from app.models.department import Department
# from app.models.payroll import Payroll
# from app.models.leave import Leave  # Optional, if you track leave requests

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    employee_count = db.query(Employee).count()
    department_count = db.query(Department).count()
    # payroll_count = db.query(Payroll).count()

    # Optional: If you have a `Leave` model and track status
    # pending_leaves = db.query(Leave).filter(Leave.status == "pending").count()

    return {
        "employees": employee_count,
        "departments": department_count,
        # "payrollEntries": payroll_count,
        # "pendingLeaves": pending_leaves   # Uncomment if Leave model is added
    }
