
import sqlite3


DB_PATH = "erp.db"

# Connect to SQLite DB (in-memory for this example)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# cursor.execute("SELECT employee_name, manager_id FROM EmployeeMaster WHERE employee_id = ?", ('1002',))
# emp_record = cursor.fetchone()
# print(emp_record)    

cursor.execute("select * from Leaves")
records = cursor.fetchall()
for row in records:
    print(row)

# Commit and close
conn.commit()
conn.close()

print("✅ Database initialized and seeded successfully!")

