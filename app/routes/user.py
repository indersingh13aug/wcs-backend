from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.models.employee import Employee
from app.schemas.user import UserCreate,  UserOut
from app.database import get_db
from app.routes.auth import get_current_user
from passlib.context import CryptContext
from pydantic import BaseModel

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Ensure it only adds handlers once
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(name)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler) 


class PasswordChange(BaseModel):
    current_password: str
    new_password: str


@router.get("/check-username")
def check_username(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    return {"available": user is None}

class UsernameUpdate(BaseModel):
    username: str

@router.put("/change-username")
def change_username(data: UsernameUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Check if username already exists
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    user.username = data.username
    db.commit()
    return {"message": "Username updated successfully"}

@router.put("/change-password")
def change_password(data: PasswordChange, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not pwd_context.verify(data.current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    user.hashed_password = pwd_context.hash(data.new_password)
    db.commit()
    return {"message": "Password changed successfully"}


@router.get("/users", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    users = (
        db.query(User, Employee, Role)
        .join(Employee, User.employee_id == Employee.id)  
        .join(Role, Role.id == Employee.role_id )      
        .filter(User.is_deleted == False)
        .all()
    )

    result = []
    for user, emp, role in users:
        full_name = " ".join(filter(None, [emp.first_name, emp.middle_name, emp.last_name])).strip()
        result.append({
            "id": user.id,
            "username": user.username,
            "employee_id": user.employee_id,  # ✅ Include this
            "employee_name": full_name,
            "is_active": user.is_active,
            "role_name": role.name,  # ✅ Include role name
        })

    return result


@router.post("/users", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(user.username)
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
