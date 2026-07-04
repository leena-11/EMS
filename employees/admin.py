from django.contrib import admin
from .models import Employee, Department, UserProfile


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'full_name', 'email', 'phone', 'department', 'designation', 'status', 'joining_date']
    list_filter = ['status', 'gender', 'department']
    search_fields = ['first_name', 'last_name', 'email', 'designation']
    ordering = ['-id']
    readonly_fields = ['employee_id', 'created_at']

    fieldsets = (
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'gender', 'date_of_birth', 'profile_photo')
        }),
        ('Job Info', {
            'fields': ('department', 'designation', 'salary', 'joining_date', 'status')
        }),
        ('Address', {
            'fields': ('address',)
        }),
        ('Meta', {
            'fields': ('employee_id', 'created_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']
    search_fields = ['user__username', 'user__email']
