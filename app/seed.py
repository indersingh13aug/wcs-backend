
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal
from datetime import date
from sqlalchemy import Column, Integer, String, Text, Date,Boolean,Float, ForeignKey,DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from datetime import datetime



# Use local SQLite file 
SQLALCHEMY_DATABASE_URL = "sqlite:///./erp.db"

# Required for SQLite (only for single-threaded use)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal will be used for DB interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    client_code=Column(String, nullable=True)
    contact_person = Column(String)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    addressline1 = Column(String, nullable=True)
    addressline2 = Column(String, nullable=True)
    state=Column(String, nullable=True)
    country =Column(String, nullable=True)
    pincode=Column(String, nullable=True)
    gst_number = Column(String)
    is_deleted = Column(Boolean, default=False)

class Sales(Base):
        __tablename__ = "sales"

        id = Column(Integer, primary_key=True, index=True)
        client_id = Column(Integer, ForeignKey("clients.id"))
        role_id = Column(Integer, ForeignKey("roles.id"))
        service_id = Column(Integer, ForeignKey("services.id"))
        type_id = Column(Integer, ForeignKey("client_types.id"))

        contact_number = Column(String, nullable=False)
        contact_person = Column(String, nullable=False)
        date = Column(Date, nullable=False)
        status = Column(String, default="lead")  # lead, opportunity, active

        is_deleted = Column(Boolean, default=False)


class GSTItems(Base):
    __tablename__ = "gst_items"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    hsn_sac = Column(String, nullable=False)
    cgst_rate = Column(Float, nullable=False, default=0.0)
    sgst_rate = Column(Float, nullable=False, default=0.0)
    igst_rate = Column(Float, nullable=False, default=0.0)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class GSTInvoice(Base):
    __tablename__ = "gst_invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, nullable=False, unique=True)

    item_id = Column(Integer, ForeignKey("gst_items.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)  # ✅ New field

    quantity = Column(Integer, nullable=False)
    rate_per_unit = Column(Float, nullable=False)

    cgst_amount = Column(Float, nullable=False)
    sgst_amount = Column(Float, nullable=False)
    igst_amount = Column(Float, nullable=False)

    total_amount = Column(Float, nullable=False)
    billing_date = Column(Date, nullable=False)

    # Relationships
    item = relationship("GSTItems", backref="invoices")
    client = relationship("Client", backref="invoices") 

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    is_active = Column(Boolean, default=True)
    is_first_time_user = Column(Boolean, default=True)

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    client_id = Column(Integer, ForeignKey("clients.id"))
    assigned_team = Column(String)  # e.g., "1,2,3"
    is_deleted = Column(Boolean, default=False)

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False)  # e.g., IN, US

class State(Base):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    is_deleted = Column(Boolean, default=False)

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)
    employees = relationship("Employee", back_populates="role")
    access = relationship("RolePageAccess", back_populates="role", cascade="all, delete")

class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    path = Column(String, unique=True)
    is_deleted = Column(Boolean, default=False)
    group_name = Column(String, unique=False,nullable=True) 
    access = relationship("RolePageAccess", back_populates="page", cascade="all, delete")


class RolePageAccess(Base):
    __tablename__ = "role_page_access"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    page_id = Column(Integer, ForeignKey("pages.id"))

    view_access = Column(Boolean, default=False)
    apply_access = Column(Boolean, default=False)
    update_access = Column(Boolean, default=False)
    delete_access = Column(Boolean, default=False)

    role = relationship("Role", back_populates="access")
    page = relationship("Page", back_populates="access")

    
class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String(255), nullable=True)
    is_deleted = Column(Boolean, default=False)

    employees = relationship("Employee", back_populates="department")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    user_id  = Column(Integer, ForeignKey("users.id"))
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_joining= Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    ro_id = Column(Integer, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    status=Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)
    # ✅ Add this relationship
    department = relationship("Department", back_populates="employees")
    leaves = relationship("Leave", back_populates="employee")
    role = relationship("Role", back_populates="employees")

class ClientType(Base):
    __tablename__ = "client_types"

    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String, unique=True, nullable=False)



class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(Text, nullable=True)
    status = Column(String(20), default="pending", nullable=False)
    type = Column(String(50), nullable=False)

    employee = relationship("Employee", back_populates="leaves")


def seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # ✅ Step 2: Hash passwords and add users
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    db = SessionLocal()
    
    country_list = [
    {"name": "Afghanistan", "code": "AF"},
    {"name": "Albania", "code": "AL"},
    {"name": "Algeria", "code": "DZ"},
    {"name": "Andorra", "code": "AD"},
    {"name": "Angola", "code": "AO"},
    {"name": "Argentina", "code": "AR"},
    {"name": "Australia", "code": "AU"},
    {"name": "Austria", "code": "AT"},
    {"name": "Bangladesh", "code": "BD"},
    {"name": "Belgium", "code": "BE"},
    {"name": "Brazil", "code": "BR"},
    {"name": "Canada", "code": "CA"},
    {"name": "China", "code": "CN"},
    {"name": "France", "code": "FR"},
    {"name": "Germany", "code": "DE"},
    {"name": "India", "code": "IN"},
    {"name": "Japan", "code": "JP"},
    {"name": "United Kingdom", "code": "GB"},
    {"name": "United States", "code": "US"},
]
    for item in country_list:
        if not db.query(Country).filter_by(code=item["code"]).first():
            db.add(Country(**item))
    db.commit()
    indian_states = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
        "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
        "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
        "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
        "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands",
        "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
        "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
    ]
    
    india = db.query(Country).filter_by(code="IN").first()
    for name in indian_states:
        if not db.query(State).filter_by(name=name, country_id=india.id).first():
            db.add(State(name=name, country_id=india.id))

    # roles
    roles = [
        Role(name="Admin"),Role(name="HR"),Role(name="BDM"),Role(name="Solution Architect"),Role(name="Lead"),Role(name="CEO"), Role(name="CTO"), Role(name="Founder"), Role(name="Purchase Manager"),
        Role(name="Developer"), Role(name="Delivery Manager"),
    ]
    db.add_all(roles)
    
    pages = [
        ("Client", "/clients","Admin"),
        ("Department", "/departments","Admin"),
        ("Employee", "/employees",""),
        ("Gst Invoice", "/gst-invoices","GST"),
        ("GST Item", "/gst-items","Admin"),
        ("Leave Master", "/leave-master","Admin"),
        ("Leave Request", "/leave-request",""),
        ("Project", "/projects","Admin"),
        ("Role", "/roles","Admin"),
        ("Sales", "/sales",""),
        ("Service", "/services","Admin"),
        ("User", "/users","Admin"),
        ("Profile", "/profile",""),
        ("Project Role", "/projectrole","")
    ]
    page_objs = [Page(name=name, path=path,group_name=group_name) for name, path,group_name in pages]
    db.add_all(page_objs)
    db.commit()
    
    role_dict = {r.name: r.id for r in db.query(Role).all()}
    page_dict = {p.name: p.id for p in db.query(Page).all()}

    def grant(role, page, view=True,apply=True, update=False, delete=False):
        return RolePageAccess(
            role_id=role_dict[role],
            page_id=page_dict[str(page)],
            view_access=view,
            apply_access=apply,
            update_access=update,
            delete_access=delete
        )

    access_data = []
    
    # Admin full access
    for page in page_dict:
        access_data.append(grant("Admin", page, True,True, True, True))
    
    # Common access to all roles (Leave Request, Profile)
    for role in roles:
        for page in ["Leave Request", "Profile"]:
            access_data.append(grant(role.name, page, True, True))

    # HR access to Employee
    access_data.append(grant("HR", "Employee", True,True, True, True))

    # BDM access to Client and Sales
    for page in ["Client", "Sales"]:
        access_data.append(grant("BDM", page, True, True,True))

    # Developer and Delivery Manager access to My_project_role
    for role in ["Developer", "Delivery Manager"]:
        access_data.append(grant(role, "Project Role", True,True))

    db.add_all(access_data)

    services = ["Web Development", "Mobile App", "AI Solution", "UI/UX Design", "Cloud Consulting"]

    for name in services:
        if not db.query(Service).filter_by(name=name).first():
            db.add(Service(name=name))

    types = ["Individual", "Company"]
    for t in types:
        if not db.query(ClientType).filter_by(type_name=t).first():
            db.add(ClientType(type_name=t))

    departments = [
        {"name": "Human Resources", "description": "Handles hiring, onboarding, and employee welfare."},
        {"name": "IT", "description": "Responsible for software development and product engineering."},
        {"name": "Sales", "description": "Manages client relationships and business development."},
        {"name": "Marketing", "description": "Focuses on market research and promotional strategies."},
        {"name": "Finance", "description": "Handles budgeting, accounting, and payroll operations."}
    ]

    for dept in departments:
        existing = db.query(Department).filter(Department.name == dept["name"]).first()
        if not existing:
            new_dept = Department(**dept)
            db.add(new_dept)
  
    users = [
    {"username": "admin", "password": "wcs-sol@2306", "employee_id":1},
    {"username": "hr", "password": "wcs-sol@2306", "employee_id":2},
    ]

    for u in users:
        hashed = pwd_context.hash(u["password"])
        db_user = User(username=u["username"], hashed_password=hashed, employee_id=u["employee_id"])
        db.add(db_user)
    db.commit()
    # Employees
    employees = [
            Employee(user_id=1, first_name="Amit", middle_name="Kumar", last_name="Sharma", date_of_joining='29-09-2010', email="amitkumar.sharma@webcore.com",ro_id=2, role_id=1, department_id=1,status='Active'),
            Employee(user_id=2, first_name="Priya", middle_name="Rani", last_name="Verma", date_of_joining='15-01-2012', email="priyarani.verma@webcore.com",ro_id=2, role_id=2, department_id=1,status='Active'),
            Employee(user_id=3, first_name="Rahul", middle_name="Singh", last_name="Yadav", date_of_joining='12-03-2015', email="rahulsingh.yadav@webcore.com",ro_id=2, role_id=3, department_id=1,status='Active'),
            Employee(user_id=4, first_name="Neha", middle_name="Kumari", last_name="Jain", date_of_joining='23-06-2016', email="nehakumari.jain@webcore.com",ro_id=1, role_id=4, department_id=2,status='Active'),
            Employee(user_id=5, first_name="Rohit", middle_name="Raj", last_name="Mishra", date_of_joining='07-07-2018', email="rohitraj.mishra@webcore.com",ro_id=2, role_id=5, department_id=2,status='Active'),
            Employee(user_id=3, first_name="Sneha", middle_name="S.", last_name="Tripathi", date_of_joining='01-01-2019', email="sneha.s.tripathi@webcore.com",ro_id=3, role_id=3, department_id=2,status='Active'),
            Employee(user_id=2, first_name="Ankit", middle_name="A.", last_name="Gupta", date_of_joining='19-05-2017', email="ankit.a.gupta@webcore.com",ro_id=1, role_id=2, department_id=2,status='Active'),
            Employee(user_id=5, first_name="Divya", middle_name="K.", last_name="Tiwari", date_of_joining='08-08-2020', email="divya.k.tiwari@webcore.com",ro_id=1, role_id=5, department_id=2,status='Active'),
            Employee(user_id=2, first_name="Swati", middle_name="D.", last_name="Nair", date_of_joining='25-05-2020', email="swati.d.nair@webcore.com",ro_id=2, role_id=2, department_id=2,status='Active')
        ]

    db.add_all(employees)

    clients = [
        {"name": "Acme Corp","client_code":"AC4567890", "contact_person": "John Doe", "email": "john@acme.com","phone": "9876543210", "gst_number": "GST12345"},
        {"name": "Globex Ltd","client_code":"56567890",  "contact_person": "Jane Smith", "email": "jane@globex.com","phone": "8765432109", "gst_number": "GST67890"},
        {"name": "Umbrella Inc","client_code":"32534364",  "contact_person": "Alice", "email": "alice@umbrella.com","phone": "7654321098", "gst_number": "GST24680"},
        {"name": "Initech","client_code":"INCDF7890",  "contact_person": "Bob", "email": "bob@initech.com","phone": "6543210987",  "gst_number": "GST13579"},
        {"name": "Soylent","client_code":"SD567890",  "contact_person": "Eve", "email": "eve@soylent.com","phone": "5432109876",  "gst_number": "GST99999"}
    ]
    client_objs = [Client(**client) for client in clients]
    db.add_all(client_objs)

    # Projects
    projects = [
        Project(name="HRMS System", description="Human Resource Management Software", client_id=1, assigned_team="4,5"),
        Project(name="E-commerce Platform", description="Multi-vendor online store", client_id=2, assigned_team="6,7"),
        Project(name="Analytics Dashboard", description="BI tool for client data", client_id=3, assigned_team="8,9"),
    ]
    db.add_all(projects)    

    # Seed GST Items
    gst_items = [
        {"item_name": "Cloud Hosting", "description": "Monthly cloud server hosting","hsn_sac": "998315", "cgst_rate": 9.0, "sgst_rate": 9.0, "igst_rate": 18.0},
        {"item_name": "Software Development", "description": "Custom software solution","hsn_sac": "998314", "cgst_rate": 9.0, "sgst_rate": 9.0, "igst_rate": 18.0},
        {"item_name": "IT Consulting", "description": "Consulting services for IT","hsn_sac": "998313", "cgst_rate": 9.0, "sgst_rate": 9.0, "igst_rate": 18.0},
        {"item_name": "Mobile App Dev", "description": "Android/iOS app development","hsn_sac": "998312", "cgst_rate": 9.0, "sgst_rate": 9.0, "igst_rate": 18.0},
        {"item_name": "Web Maintenance", "description": "Annual maintenance for websites","hsn_sac": "998316", "cgst_rate": 9.0, "sgst_rate": 9.0, "igst_rate": 18.0},
    ]

    gst_item_objs = [GSTItems(**item) for item in gst_items]
    db.add_all(gst_item_objs)
    db.commit()

    # Fetch inserted items
    gst_item_objs = db.query(GSTItems).all()

    # Seed Invoices (1 per client for demo)
    invoice_data = []
    for i in range(len(client_objs)):
        item = gst_item_objs[i % len(gst_item_objs)]
        qty = 10 + i
        rate = 1000.0 + (i * 100)

        cgst_amt = (rate * qty) * (item.cgst_rate / 100)
        sgst_amt = (rate * qty) * (item.sgst_rate / 100)
        igst_amt = (rate * qty) * (item.igst_rate / 100)
        total = (rate * qty) + cgst_amt + sgst_amt + igst_amt

        invoice_data.append(GSTInvoice(
            invoice_number=f"INV00{i+1}",
            item_id=item.id,
            client_id=client_objs[i].id,
            quantity=qty,
            rate_per_unit=rate,
            cgst_amount=cgst_amt,
            sgst_amount=sgst_amt,
            igst_amount=igst_amt,
            total_amount=total,
            billing_date=date.today()
        ))

    db.add_all(invoice_data)

    
    db.commit()
    db.close()
    print("🌱 Sample data created")

if __name__ == "__main__":
    seed()
