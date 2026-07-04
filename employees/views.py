from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Employee, Department, UserProfile
from .forms import EmployeeForm, DepartmentForm, ProfileForm, RegistrationForm
from django.contrib.auth.models import User


# ─────────────────────────────────────────────
#  AUTH VIEWS
# ─────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'employees/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            messages.success(request, "Account created! Please login.")
            return redirect('login')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RegistrationForm()
    return render(request, 'employees/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# ─────────────────────────────────────────────
#  DASHBOARD
# ─────────────────────────────────────────────

@login_required
def dashboard_view(request):
    total_employees = Employee.objects.count()
    active_employees = Employee.objects.filter(status='Active').count()
    inactive_employees = Employee.objects.filter(status='Inactive').count()
    male_employees = Employee.objects.filter(gender='Male').count()
    female_employees = Employee.objects.filter(gender='Female').count()
    recent_employees = Employee.objects.select_related('department').order_by('-id')[:5]

    context = {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'inactive_employees': inactive_employees,
        'male_employees': male_employees,
        'female_employees': female_employees,
        'recent_employees': recent_employees,
    }
    return render(request, 'employees/dashboard.html', context)


# ─────────────────────────────────────────────
#  EMPLOYEE VIEWS
# ─────────────────────────────────────────────

@login_required
def employee_list_view(request):
    query = request.GET.get('q', '')
    department_filter = request.GET.get('department', '')
    status_filter = request.GET.get('status', '')
    sort = request.GET.get('sort', '-id')

    employees = Employee.objects.select_related('department').all()

    if query:
        employees = employees.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(designation__icontains=query) |
            Q(department__name__icontains=query)
        )
    if department_filter:
        employees = employees.filter(department__id=department_filter)
    if status_filter:
        employees = employees.filter(status=status_filter)

    # Sort
    valid_sorts = ['id', '-id', 'first_name', '-first_name', 'department__name', 'status']
    if sort in valid_sorts:
        employees = employees.order_by(sort)
    else:
        employees = employees.order_by('-id')

    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    departments = Department.objects.all()

    context = {
        'page_obj': page_obj,
        'query': query,
        'department_filter': department_filter,
        'status_filter': status_filter,
        'sort': sort,
        'departments': departments,
        'total_count': employees.count(),
    }
    return render(request, 'employees/employee_list.html', context)


@login_required
def employee_detail_view(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})


@login_required
def employee_add_view(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f"Employee {employee.full_name} added successfully!")
            return redirect('employee_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Add Employee', 'btn_label': 'Save Employee'})


@login_required
def employee_update_view(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, f"Employee {employee.full_name} updated successfully!")
            return redirect('employee_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Edit Employee', 'employee': employee, 'btn_label': 'Update Employee'})


@login_required
def employee_delete_view(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        name = employee.full_name
        employee.delete()
        messages.success(request, f"Employee {name} deleted successfully!")
        return redirect('employee_list')
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})


# ─────────────────────────────────────────────
#  DEPARTMENT VIEWS
# ─────────────────────────────────────────────

@login_required
def department_list_view(request):
    departments = Department.objects.all()
    paginator = Paginator(departments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'employees/department_list.html', {'page_obj': page_obj})


@login_required
def department_add_view(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department added successfully!")
            return redirect('department_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DepartmentForm()
    return render(request, 'employees/department_form.html', {'form': form, 'title': 'Add Department'})


@login_required
def department_edit_view(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully!")
            return redirect('department_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'employees/department_form.html', {'form': form, 'title': 'Edit Department', 'department': department})


@login_required
def department_delete_view(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        messages.success(request, "Department deleted successfully!")
        return redirect('department_list')
    return render(request, 'employees/department_confirm_delete.html', {'department': department})


# ─────────────────────────────────────────────
#  PROFILE VIEWS
# ─────────────────────────────────────────────

@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'employees/profile.html', {'profile': profile})


@login_required
def profile_update_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            profile = form.save(commit=False)
            # update User fields
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.email = form.cleaned_data.get('email', '')
            request.user.save()
            profile.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile, user=request.user)
    return render(request, 'employees/profile_form.html', {'form': form, 'profile': profile})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'
        field.widget.attrs['placeholder'] = field.label
    return render(request, 'employees/change_password.html', {'form': form})


# ─────────────────────────────────────────────
#  ERROR HANDLERS
# ─────────────────────────────────────────────

def handler404(request, exception):
    return render(request, 'employees/404.html', status=404)


def handler500(request):
    return render(request, 'employees/500.html', status=500)
