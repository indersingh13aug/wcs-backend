import secrets
print(secrets.token_urlsafe(32))

import sqlite3
DB_PATH = "erp.db"

# Connect to SQLite DB (in-memory for this example)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# cursor.execute("SELECT employee_name, manager_id FROM EmployeeMaster WHERE employee_id = ?", ('1002',))
# emp_record = cursor.fetchone()
# print(emp_record)  
print('***************gst_items***************')  
cursor.execute("SELECT * FROM gst_items")
records = cursor.fetchall()
for row in records:
    print(row)

print('**************gst_invoices****************')
cursor.execute("SELECT * FROM gst_invoices")
records = cursor.fetchall()
for row in records:
    print(row)
print('**************gst_invoice_items****************')
cursor.execute("SELECT * FROM gst_invoice_items")
records = cursor.fetchall()
for row in records:
    print(row)

# Commit and close
conn.commit()
conn.close()

