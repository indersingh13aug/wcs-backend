from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use local SQLite file 
# SQLALCHEMY_DATABASE_URL = "sqlite:////erp.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///./app/erp.db"

# Required for SQLite (only for single-threaded use)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# SessionLocal will be used for DB interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Dependency to get DB session (used with Depends)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
