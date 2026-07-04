# Employee Management System

## Project Overview

The **Employee Management System** is a web-based application developed using **Django**. It helps administrators efficiently manage employee records through a simple and user-friendly interface. The system provides secure authentication and allows performing all essential employee management operations such as adding, updating, deleting, viewing, and searching employee information.

---

# Features

* Secure Login System
* Admin Dashboard
* Add Employee
* View Employee Details
* Update Employee Information
* Delete Employee
* Search Employee
* Responsive User Interface

---

# Technologies Used

* **Backend:** Django
* **Database:** Django Models (SQLite)
* **Frontend:** HTML5, CSS3, Bootstrap
* **Programming Language:** Python

---

# Modules

## 1. Authentication Module

* Admin Login
* Logout

## 2. Employee Management Module

* Add Employee
* View Employees
* Update Employee
* Delete Employee
* Search Employee

## 3. Dashboard Module

* Display Total Employees
* Employee Management Shortcuts

---

# Employee Information

The application stores the following employee details:

* Employee ID
* Full Name
* Email Address
* Phone Number
* Department
* Designation
* Salary
* Date of Joining

---

# Project Structure

```text
EmployeeManagement/
│
├── EmployeeManagement/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── employees/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── apps.py
│
├── db.sqlite3
├── manage.py
└── README.md
```

---

# Django Model

```python
from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    joining_date = models.DateField()

    def __str__(self):
        return self.name
```

---

# Workflow

```text
Admin Login
      │
      ▼
Dashboard
      │
      ▼
Employee Management
      │
 ┌────┼────┐
 ▼    ▼    ▼
Add  Update Delete
      │
      ▼
Search Employee
      │
      ▼
Logout
```

---

# Future Enhancements

* Employee Profile Photos
* Attendance Management
* Payroll Management
* Leave Management
* Role-Based Access Control
* Export Employee Records to Excel/PDF

---

# Conclusion

The **Employee Management System** is a simple and efficient Django-based web application for managing employee records. It provides secure authentication, organized employee data management, and an intuitive interface. The project demonstrates the implementation of Django Models, CRUD operations, authentication, and responsive web design, making it a suitable mini project for learning Django web development.
