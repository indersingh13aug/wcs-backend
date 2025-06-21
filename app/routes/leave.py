from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.leave import Leave
from app.schemas.leave import LeaveCreate, LeaveUpdate, LeaveOut
from app.database import get_db
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Ensure it only adds handlers once
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(name)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


router = APIRouter()

# 🔸 Create new leave request
@router.post("/leaves", response_model=LeaveOut)
def create_leave(leave: LeaveCreate, db: Session = Depends(get_db)):
    logger.info(f"User request: {leave}")

    new_leave = Leave(**leave.dict())
    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)
    return new_leave

# 🔸 Get all leave records
@router.get("/leaves", response_model=list[LeaveOut])
def get_leaves(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Leave).offset(skip).limit(limit).all()

# 🔸 Get leave by ID
@router.get("/leaves/{employee_id}", response_model=LeaveOut)
def get_leave_empid(employee_id: int, db: Session = Depends(get_db)):
    leave = db.query(Leave).filter(Leave.employee_id == employee_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    return leave

# 🔸 Get leave by ID
@router.get("/leaves/{leave_id}", response_model=LeaveOut)
def get_leave(leave_id: int, db: Session = Depends(get_db)):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    return leave

# 🔸 Update leave
@router.put("/leaves/{leave_id}", response_model=LeaveOut)
def update_leave(leave_id: int, updated: LeaveUpdate, db: Session = Depends(get_db)):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(leave, key, value)
    db.commit()
    db.refresh(leave)
    return leave

# 🔸 Soft delete
@router.delete("/leaves/{leave_id}")
def delete_leave(leave_id: int, db: Session = Depends(get_db)):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    leave.is_deleted = True
    db.commit()
    return {"message": "Leave soft-deleted"}
