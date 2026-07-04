"""
Seed script — creates admin user + sample departments + employees.
Run: python seed_data.py
"""
import os
import sys
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmployeeManagement.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from employees.models import Department, Employee, UserProfile

# ── Admin user ──
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    UserProfile.objects.get_or_create(user=admin)
    print("✅ Superuser created  →  username: admin | password: admin123")
else:
    print("ℹ️  Admin user already exists.")

# ── Departments ──
dept_data = [
    ('IT',        'Information Technology'),
    ('HR',        'Human Resources'),
    ('Finance',   'Finance Department'),
    ('Marketing', 'Marketing Department'),
    ('Operations','Operations Department'),
]
depts = {}
for name, desc in dept_data:
    d, _ = Department.objects.get_or_create(name=name, defaults={'description': desc})
    depts[name] = d
print(f"✅ {len(depts)} departments ready.")

# ── Employees ──
emp_data = [
    ('John',    'Doe',     'john@example.com',    '9876543210', 'Male',   date(1990,5,15),  'IT',        'Software Engineer',   60000, date(2024,5,1),  '123 Main St, City, Country', 'Active'),
    ('Jane',    'Smith',   'jane@example.com',    '9876543211', 'Female', date(1988,4,20),  'HR',        'HR Manager',          75000, date(2024,4,25), '456 Park Ave, City, Country','Active'),
    ('Michael', 'Brown',   'michael@example.com', '9876543212', 'Male',   date(1992,3,10),  'Finance',   'Accountant',          55000, date(2024,4,7),  '789 Lake Rd, City, Country', 'Inactive'),
    ('Emily',   'Davis',   'emily@example.com',   '9876543213', 'Female', date(1995,7,22),  'Marketing', 'Marketing Executive',  48000, date(2024,4,6),  '321 River Dr, City, Country','Active'),
    ('William', 'Johnson', 'william@example.com', '9876543214', 'Male',   date(1985,11,30), 'IT',        'System Analyst',       65000, date(2024,4,5),  '654 Hill Blvd, City, Country','Active'),
]

created = 0
for fn, ln, email, ph, gen, dob, dept_name, desig, sal, jd, addr, status in emp_data:
    if not Employee.objects.filter(email=email).exists():
        Employee.objects.create(
            first_name=fn, last_name=ln, email=email, phone=ph,
            gender=gen, date_of_birth=dob,
            department=depts.get(dept_name),
            designation=desig, salary=sal, joining_date=jd,
            address=addr, status=status
        )
        created += 1

print(f"✅ {created} sample employees created (skipped existing).")
print("\n🚀 Ready! Run:  python manage.py runserver")
print("   Login at:    http://127.0.0.1:8000/login/")
print("   Admin at:    http://127.0.0.1:8000/admin/")
