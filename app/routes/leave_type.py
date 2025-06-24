from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.leave_type import LeaveType
from app.schemas.leave_type import LeaveTypeCreate, LeaveTypeUpdate, LeaveTypeOut

router = APIRouter()

@router.get("/leave-types", response_model=list[LeaveTypeOut])
def get_leave_types(db: Session = Depends(get_db)):
    return db.query(LeaveType).all()

@router.post("/leave-types", response_model=LeaveTypeOut)
def create_leave_type(data: LeaveTypeCreate, db: Session = Depends(get_db)):
    lt = LeaveType(**data.dict())
    db.add(lt)
    db.commit()
    db.refresh(lt)
    return lt

@router.put("/leave-types/{id}", response_model=LeaveTypeOut)
def update_leave_type(id: int, data: LeaveTypeUpdate, db: Session = Depends(get_db)):
    lt = db.query(LeaveType).filter(LeaveType.id == id).first()
    if not lt:
        raise HTTPException(status_code=404, detail="Leave type not found")
    for key, value in data.dict().items():
        setattr(lt, key, value)
    db.commit()
    return lt

@router.put("/leave-types/{id}/activate")
def activate_leave_type(id: int, db: Session = Depends(get_db)):
    lt = db.query(LeaveType).filter(LeaveType.id == id).first()
    if not lt:
        raise HTTPException(status_code=404, detail="Leave type not found")
    lt.is_deleted = False
    db.commit()
    return {"message": "Activated"}

@router.put("/leave-types/{id}/deactivate")
def deactivate_leave_type(id: int, db: Session = Depends(get_db)):
    lt = db.query(LeaveType).filter(LeaveType.id == id).first()
    if not lt:
        raise HTTPException(status_code=404, detail="Leave type not found")
    lt.is_deleted = True
    db.commit()
    return {"message": "Deactivated"}
