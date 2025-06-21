from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.models.employee import Employee
from app.database import get_db
from app.models.user import User
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

SECRET_KEY = "webcore_super_secret_jwt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    role: str
    username: str
    id : int

class RefreshRequest(BaseModel):
    refresh_token: str

def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    logger.info(f"User found: {user}")

    if not user or not pwd_context.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {"sub": user.username, "role_id": user.role_id}
    access_token = create_token(payload, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_token(payload, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    # Fetch employee info (assuming `user.id` == employee.user_id)
    employee = db.query(Employee).filter(Employee.user_id == user.id, Employee.role_id == user.role_id).first()
    logger.info(f"employee found: {employee}")
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role_id": user.role_id,
        "username": user.username,
        "id":user.id,
        "employee": {
            "id": employee.id,
            "user_id": employee.user_id,
            "first_name": employee.first_name,
            "middle_name": employee.middle_name,
            "last_name": employee.last_name,
            "date_of_joining": employee.date_of_joining,
            "email": employee.email,
            "role_id": employee.role_id,
            "department_id": employee.department_id,
            "status": employee.status,
        } if employee else None
    }

@router.post("/refresh")
def refresh_token(request: RefreshRequest):
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")

        if not username or not role:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        new_access = create_token(
            {"sub": username, "role": role},
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"access_token": new_access}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
