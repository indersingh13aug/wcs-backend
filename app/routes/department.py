from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.department import Department
from app.schemas.department import DepartmentOut  # create if not available
from app.database import get_db

router = APIRouter()

@router.get("/departments", response_model=list[DepartmentOut])
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).filter(Department.is_deleted == False).all()
