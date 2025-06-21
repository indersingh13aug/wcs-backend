from fastapi import FastAPI
from app.database import engine, Base
from app.routes import employee as employee_routes
from app.routes import role as role_routes
from app.routes import department as department_routes
from app.routes import client as client_routes
from app.routes import project as project_routes
from app.routes import leave as leave_routes
from app.routes import auth as auth_routes
from app.routes import user as user_routes
from app.routes import dashboard 
from app.routes import gst_receipt as gst_receipt_routes

from fastapi.middleware.cors import CORSMiddleware
from app.logging_config import setup_logging

setup_logging()

import logging
logger = logging.getLogger(__name__)



app = FastAPI(
    title="WebCore ERP API"
    # ,docs_url="/docs",
    # redoc_url="/redoc",
    # openapi_url="/openapi.json"
)

# Allow frontend origin
origins = [
    #  "https://wcs-erp.netlify.app",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["*"] for development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables if not exist
Base.metadata.create_all(bind=engine)

# Register API routes
app.include_router(auth_routes.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(employee_routes.router, prefix="/api")
app.include_router(project_routes.router, prefix="/api")
app.include_router(client_routes.router, prefix="/api")
app.include_router(department_routes.router, prefix="/api")
app.include_router(leave_routes.router, prefix="/api")
app.include_router(role_routes.router, prefix="/api")
app.include_router(user_routes.router, prefix="/api")
app.include_router(gst_receipt_routes.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to WebCore AI ERP Backend!"}
