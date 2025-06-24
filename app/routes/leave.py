from fastapi import APIRouter, Depends, HTTPException,Body
from sqlalchemy.orm import Session
from app.models.leave import Leave
from app.models.employee import Employee
from app.schemas.leave import LeaveCreate, LeaveUpdate, LeaveOut
from app.database import get_db
import logging
from app.models.leave_type import LeaveType

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

from sqlalchemy.orm import joinedload

@router.get("/leaves_req")
def get_leaves(employee_id: int, db: Session = Depends(get_db)):
    leaves = (
        db.query(Leave)
        .options(joinedload(Leave.leave_type))  # ✅ JOIN the leave type
        .filter(Leave.employee_id == employee_id)
        .all()
    )

    results = []
    for leave in leaves:
        results.append({
            "id": leave.id,
            "employee_id": leave.employee_id,
            "start_date": leave.start_date,
            "end_date": leave.end_date,
            "reason": leave.reason,
            "status": leave.status,
            "leave_type_id": leave.leave_type_id,
            "leave_type": {
                "id": leave.leave_type.id,
                "name": leave.leave_type.name
            } if leave.leave_type else None
        })

    return results



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

@router.get("/leave-worklist/{ro_id}")
def get_pending_leaves_for_ro(ro_id: int, db: Session = Depends(get_db)):
    # Find all employees whose ro_id matches the given ro_id
    subordinates = db.query(Employee).filter(Employee.ro_id == ro_id).all()
    emp_ids = [emp.id for emp in subordinates]

    if not emp_ids:
        return []

    # Fetch all pending leaves for those employees
    leaves = (
        db.query(Leave)
        .options(joinedload(Leave.employee), joinedload(Leave.leave_type))
        .filter(Leave.employee_id.in_(emp_ids), Leave.status == "Pending")
        .all()
    )

    result = []
    for leave in leaves:
        result.append({
            "id": leave.id,
            "employee_name": f"{leave.employee.first_name} {leave.employee.last_name}",
            "leave_type": leave.leave_type.name if leave.leave_type else "N/A",
            "start_date": leave.start_date,
            "end_date": leave.end_date,
            "reason": leave.reason,
            "status": leave.status,
        })

    return result

@router.put("/leaves/{leave_id}/status")
def update_leave_status(leave_id: int, status: str = Body(...), db: Session = Depends(get_db)):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    if status not in ["Approved", "Rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    leave.status = status
    db.commit()
    return {"message": f"Leave {status.lower()} successfully."}


@router.get("/leaves-summary")
def get_leave_summary(employee_id: int, db: Session = Depends(get_db)):
    leave_types = db.query(LeaveType).filter(LeaveType.is_deleted == False).all()
    leaves = db.query(Leave).filter(Leave.employee_id == employee_id).all()

    summary = []

    for lt in leave_types:
        applied = [l for l in leaves if l.leave_type_id == lt.id]
        pending = len([l for l in applied if l.status == "Pending"])
        approved = len([l for l in applied if l.status == "Approved"])
        total = lt.max_days

        summary.append({
            "leave_type_id": lt.id,
            "leave_type_name": lt.name,
            "total_leaves": total,
            "applied_leaves": len(applied),
            "pending_leaves": pending,
            "approved_leaves": approved,
            "remaining_leaves": total - (pending + approved)
        })

    return summary
