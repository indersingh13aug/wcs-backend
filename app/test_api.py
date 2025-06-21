# run_create_user.py

from sqlalchemy.orm import Session
from database import SessionLocal  # your SQLAlchemy session
from passlib.context import CryptContext
from fastapi import HTTPException
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from sqlalchemy import Column, Integer, String,Boolean,ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    employee_id = Column(Integer,nullable=False)
    is_active = Column(Boolean, default=True)
# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session):
    existing = db.query(User).filter(User.username == "test").first()
    logger.info(f"Creating user, existing: {existing}")
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = pwd_context.hash("wcs@123")
    new_user = User(
        username="test",
        hashed_password=hashed_password,
        employee_id=3,
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Main runner
if __name__ == "__main__":
    db = SessionLocal()
    try:
        user = create_user(db)
        print("User created:", user.username)
    except HTTPException as e:
        print("Error:", e.detail)
    finally:
        db.close()
