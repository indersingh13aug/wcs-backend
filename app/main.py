from fastapi import FastAPI
from app.database import engine, Base
from app.routes import employee, role,department,client,client_type,project,leave,auth,user,dashboard,gst_invoice,gst_item, country, state, page, role_access,role_user_map,service,sales,client_type ,leave_type, project_employee_map, task, task_assignment,task_comments
from fastapi.middleware.cors import CORSMiddleware
from app.logging_config import setup_logging
from app.config import settings

from fastapi.staticfiles import StaticFiles

setup_logging()

import logging
logger = logging.getLogger(__name__)


app = FastAPI(
    title="WebCore ERP API"
    ,docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    debug=settings.DEBUG
)


# Allow frontend origin
origins = [
    "https://wcs-erp.netlify.app",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
@app.get("/info")
def info():
    return {
        "env": settings.ENV,
        "debug": settings.DEBUG,
        # "db_url": settings.DATABASE_URL,
        "wkhtmltopdf_path": settings.WKHTMLTOPDF_PATH
    }

# Create DB tables if not exist
Base.metadata.create_all(bind=engine)

# Register API routes
app.include_router(auth.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(employee.router, prefix="/api")
app.include_router(project.router, prefix="/api")
app.include_router(client.router, prefix="/api")
app.include_router(client_type.router, prefix="/api")
app.include_router(department.router, prefix="/api")
app.include_router(leave.router, prefix="/api")
app.include_router(role.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(gst_invoice.router, prefix="/api")
app.include_router(gst_item.router, prefix="/api")
app.include_router(state.router, prefix="/api")
app.include_router(country.router, prefix="/api")
app.include_router(page.router, prefix="/api")
app.include_router(role_access.router, prefix="/api")
app.include_router(service.router, prefix="/api")
app.include_router(sales.router, prefix="/api")
app.include_router(role_user_map.router, prefix="/api")
app.include_router(leave_type.router, prefix="/api")
app.include_router(project_employee_map.router, prefix="/api")
app.include_router(task.router, prefix="/api")
app.include_router(task_assignment.router, prefix="/api")
app.include_router(task_comments.router, prefix="/api")
@app.get("/")
def root():
    return {"message": "Welcome to WebCore AI ERP Backend!"}
