import os
import django
from decimal import Decimal
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmployeeManagement.settings')
django.setup()

from django.contrib.auth.models import User
from employees.models import Employee

def populate():
    # 1. Create Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser 'admin' with password 'admin123' created successfully.")
    else:
        print("Superuser 'admin' already exists.")

    # 2. Create Dummy Employees
    dummy_employees = [
        {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '123-456-7890',
            'department': 'Engineering',
            'designation': 'Senior Software Engineer',
            'salary': Decimal('95000.00'),
            'joining_date': date(2024, 3, 15)
        },
        {
            'name': 'Jane Smith',
            'email': 'jane.smith@example.com',
            'phone': '987-654-3210',
            'department': 'Product',
            'designation': 'Product Manager',
            'salary': Decimal('105000.00'),
            'joining_date': date(2023, 10, 1)
        },
        {
            'name': 'Alice Johnson',
            'email': 'alice.j@example.com',
            'phone': '555-019-2834',
            'department': 'Design',
            'designation': 'UI/UX Designer',
            'salary': Decimal('85000.00'),
            'joining_date': date(2025, 1, 10)
        },
        {
            'name': 'Bob Miller',
            'email': 'bob.miller@example.com',
            'phone': '444-222-1111',
            'department': 'Engineering',
            'designation': 'QA Engineer',
            'salary': Decimal('75000.00'),
            'joining_date': date(2025, 2, 20)
        },
        {
            'name': 'Sarah Connor',
            'email': 'sarah.c@example.com',
            'phone': '777-888-9999',
            'department': 'Operations',
            'designation': 'Operations Director',
            'salary': Decimal('125000.00'),
            'joining_date': date(2022, 6, 1)
        }
    ]

    for emp_data in dummy_employees:
        emp, created = Employee.objects.get_or_create(
            email=emp_data['email'],
            defaults=emp_data
        )
        if created:
            print(f"Created dummy employee: {emp.name}")
        else:
            print(f"Employee {emp.name} already exists.")

    print("Database population completed successfully!")

if __name__ == '__main__':
    populate()
