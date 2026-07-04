#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Direct injection of the correct Python site-packages path to guarantee Django is found
sys.path.insert(0, r"C:\Users\jarap\AppData\Local\Programs\Python\Python313\Lib\site-packages")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmployeeManagement.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
