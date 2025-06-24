from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.models.user import User
from app.models.employee import Employee
from app.schemas.user import UserCreate, UserUpdate, UserOut
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

@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).options(joinedload(User.employee)).all()
    return [
        UserOut(
            id=u.id,
            username=u.username,
            employee_id=u.employee_id,
            is_active=u.is_active
            , employee_name=f"{u.employee.first_name} {u.employee.middle_name or ''} {u.employee.last_name}".strip()
        )
        for u in users
    ]

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/users", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Calling create_user")
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = pwd_context.hash("wcs-sol@2306")
    logger.info(f"Creating user {user.username} Employee ID: {user.employee_id} ")
    print(f"Creating user {user.username} Employee ID: {user.employee_id} ")
    new_user = User(
        username=user.username,
        hashed_password=hashed_password,
        employee_id=user.employee_id,
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # fetch employee for name
    emp = db.query(Employee).filter(Employee.id == new_user.employee_id).first()
    full_name = " ".join(filter(None, [emp.first_name, emp.middle_name, emp.last_name]))

    return UserOut(
        id=new_user.id,
        username=new_user.username,
        employee_id=new_user.employee_id,
        is_active=new_user.is_active,
        employee_name=full_name.strip()
    )



# @router.put("/users/{user_id}", response_model=UserOut)
# def update_user(user_id: int, updated: UserUpdate, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     user.username = updated.username
#     user.employee_id = updated.employee_id
#     db.commit()
#     db.refresh(user)
#     emp = db.query(Employee).filter(Employee.id == user.employee_id).first()
#     return UserOut(id=user.id, username=user.username, employee_id=user.employee_id,
#                    is_active=user.is_active,
#                    employee_name=f"{emp.first_name} {emp.middle_name or ''} {emp.last_name}".strip())

# @router.put("/users/{user_id}/deactivate")
# def deactivate_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     user.is_active = False
#     db.commit()
#     return {"message": "User deactivated"}

# @router.put("/users/{user_id}/activate")
# def activate_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     user.is_active = True
#     db.commit()
#     return {"message": "User activated"}
