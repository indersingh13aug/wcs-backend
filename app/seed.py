
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal
from datetime import date
from sqlalchemy import Column, Integer, String, Date,Boolean,Float, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

# Use local SQLite file named erp.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./erp.db"

# Required for SQLite (only for single-threaded use)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

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


class GSTInvoice(Base):
    __tablename__ = "gst_invoices"
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, index=True)
    date = Column(Date)
    company_name = Column(String)
    company_gstin = Column(String)
    client_name = Column(String)
    client_gstin = Column(String)
    total_amount = Column(Float)
    cgst = Column(Float)
    sgst = Column(Float)
    igst = Column(Float)
    final_amount = Column(Float)

    items = relationship("GSTInvoiceItem", back_populates="invoice")

class GSTInvoiceItem(Base):
    __tablename__ = "gst_invoice_items"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("gst_invoices.id"))
    description = Column(String)
    hsn_sac = Column(String)
    quantity = Column(Integer)
    rate = Column(Float)
    amount = Column(Float)

    invoice = relationship("GSTInvoice", back_populates="items")


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    gst_number = Column(String, nullable=True)
    company = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    is_active = Column(Boolean, default=True)

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    client_id = Column(Integer, ForeignKey("clients.id"))
    assigned_team = Column(String)  # e.g., "1,2,3"
    is_deleted = Column(Boolean, default=False)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    user_id  = Column(Integer, ForeignKey("users.id"))
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_joining= Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    status=Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)

def seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # ✅ Step 2: Hash passwords and add users
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    db = SessionLocal()

    # roles
    roles = [
        Role(name="Admin"),
        Role(name="HR"),
        Role(name="BDM"),
        Role(name="Solution Architect"),
        Role(name="Lead"),
    ]

    db.add_all(roles)
 
    # roles
    departments = [
        Department(name="Admin"),
        Department(name="HR"),
        Department(name="IT"),
    ]

    db.add_all(departments)

    users = [
    {"username": "admin", "password": "admin123", "role_id":1},
    {"username": "hr", "password": "hr123", "role_id":2},
    ]

    for u in users:
        hashed = pwd_context.hash(u["password"])
        db_user = User(username=u["username"], hashed_password=hashed, role_id=u["role_id"])
        db.add(db_user)

    # db.add_all(users)
    

    # Employees
    employees = [
            Employee(user_id=1, first_name="Amit", middle_name="Kumar", last_name="Sharma", date_of_joining='29-09-2010', email="amitkumar.sharma@webcore.com", role_id=1, department_id=1,status='Active'),
            Employee(user_id=2, first_name="Priya", middle_name="Rani", last_name="Verma", date_of_joining='15-01-2012', email="priyarani.verma@webcore.com", role_id=2, department_id=1,status='Active'),
            Employee(user_id=3, first_name="Rahul", middle_name="Singh", last_name="Yadav", date_of_joining='12-03-2015', email="rahulsingh.yadav@webcore.com", role_id=3, department_id=2,status='Active'),
            Employee(user_id=4, first_name="Neha", middle_name="Kumari", last_name="Jain", date_of_joining='23-06-2016', email="nehakumari.jain@webcore.com", role_id=4, department_id=2,status='Active'),
            Employee(user_id=5, first_name="Rohit", middle_name="Raj", last_name="Mishra", date_of_joining='07-07-2018', email="rohitraj.mishra@webcore.com", role_id=5, department_id=3,status='Active'),
            Employee(user_id=3, first_name="Sneha", middle_name="S.", last_name="Tripathi", date_of_joining='01-01-2019', email="sneha.s.tripathi@webcore.com", role_id=3, department_id=1,status='Active'),
            Employee(user_id=2, first_name="Ankit", middle_name="A.", last_name="Gupta", date_of_joining='19-05-2017', email="ankit.a.gupta@webcore.com", role_id=2, department_id=2,status='Active'),
            Employee(user_id=5, first_name="Divya", middle_name="K.", last_name="Tiwari", date_of_joining='08-08-2020', email="divya.k.tiwari@webcore.com", role_id=5, department_id=1,status='Active'),
            Employee(user_id=3, first_name="Sumit", middle_name="R.", last_name="Kapoor", date_of_joining='20-02-2021', email="sumit.r.kapoor@webcore.com", role_id=3, department_id=3,status='Active'),
            Employee(user_id=4, first_name="Anjali", middle_name="M.", last_name="Bansal", date_of_joining='11-11-2016', email="anjali.m.bansal@webcore.com", role_id=4, department_id=3,status='Active'),
            Employee(user_id=5, first_name="Karan", middle_name="S.", last_name="Deshmukh", date_of_joining='10-10-2014', email="karan.s.deshmukh@webcore.com", role_id=5, department_id=1,status='Active'),
            Employee(user_id=3, first_name="Pooja", middle_name="N.", last_name="Joshi", date_of_joining='17-09-2013', email="pooja.n.joshi@webcore.com", role_id=3, department_id=2,status='Active'),
            Employee(user_id=2, first_name="Abhishek", middle_name="M.", last_name="Srivastava", date_of_joining='13-12-2022', email="abhishek.m.srivastava@webcore.com", role_id=2, department_id=2,status='Active'),
            Employee(user_id=4, first_name="Megha", middle_name="T.", last_name="Pandey", date_of_joining='04-04-2021', email="megha.t.pandey@webcore.com", role_id=4, department_id=3,status='Active'),
            Employee(user_id=1, first_name="Suresh", middle_name="P.", last_name="Rathi", date_of_joining='31-01-2010', email="suresh.p.rathi@webcore.com", role_id=1, department_id=1,status='Active'),
            Employee(user_id=3, first_name="Ritika", middle_name="V.", last_name="Singhania", date_of_joining='02-03-2023', email="ritika.v.singhania@webcore.com", role_id=3, department_id=2,status='Active'),
            Employee(user_id=5, first_name="Deepak", middle_name="L.", last_name="Kumar", date_of_joining='26-06-2019', email="deepak.l.kumar@webcore.com", role_id=5, department_id=2,status='Active'),
            Employee(user_id=3, first_name="Nikita", middle_name="A.", last_name="Mehra", date_of_joining='14-07-2017', email="nikita.a.mehra@webcore.com", role_id=3, department_id=1,status='Active'),
            Employee(user_id=4, first_name="Tarun", middle_name="R.", last_name="Chauhan", date_of_joining='09-09-2011', email="tarun.r.chauhan@webcore.com", role_id=4, department_id=3,status='Active'),
            Employee(user_id=2, first_name="Swati", middle_name="D.", last_name="Nair", date_of_joining='25-05-2020', email="swati.d.nair@webcore.com", role_id=2, department_id=2,status='Active')
        ]

    db.add_all(employees)

    # Clients
    clients = [
        Client(name="Infospark Ltd", email="contact@infospark.com", gst_number="29ABCDE1234F2Z5", company="Infospark"),
        Client(name="TechNova", email="sales@technova.com", gst_number="07XYZPQ6789M1Z3", company="TechNova Inc"),
        Client(name="Bright Solutions", email="hello@brightsol.com", gst_number="19AAQPM4567R1Z8", company="Bright Solutions Pvt Ltd"),
    ]
    db.add_all(clients)

    # Projects
    projects = [
        Project(name="HRMS System", description="Human Resource Management Software", client_id=1, assigned_team="1,2,3"),
        Project(name="E-commerce Platform", description="Multi-vendor online store", client_id=2, assigned_team="1,5,6"),
        Project(name="Analytics Dashboard", description="BI tool for client data", client_id=3, assigned_team="3,4,6"),
    ]
    db.add_all(projects)


    # Check if invoices already exist
    if db.query(GSTInvoice).first():
        print("Invoices already exist. Skipping seeding.")
        return

    invoice = GSTInvoice(
        invoice_number="INV-001",
        client_name="ABC Tech Pvt Ltd",
        date=date.today(),
        final_amount=5900.00
    )

    items = [
        GSTInvoiceItem(description="Software Development Services", amount=5000.00),
        GSTInvoiceItem(description="18% GST", amount=900.00)
    ]

    invoice.items = items

    db.add(invoice)

    db.commit()
    db.close()
    print("🌱 Sample data seeded into erp.db")

if __name__ == "__main__":
    seed()
