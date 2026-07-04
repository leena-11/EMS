from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('', views.dashboard_view, name='dashboard'),

    # Employee
    path('employees/', views.employee_list_view, name='employee_list'),
    path('employees/add/', views.employee_add_view, name='employee_add'),
    path('employees/<int:pk>/', views.employee_detail_view, name='employee_detail'),
    path('employees/<int:pk>/edit/', views.employee_update_view, name='employee_edit'),
    path('employees/<int:pk>/delete/', views.employee_delete_view, name='employee_delete'),

    # Department
    path('departments/', views.department_list_view, name='department_list'),
    path('departments/add/', views.department_add_view, name='department_add'),
    path('departments/<int:pk>/edit/', views.department_edit_view, name='department_edit'),
    path('departments/<int:pk>/delete/', views.department_delete_view, name='department_delete'),

    # Profile
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_update_view, name='profile_edit'),
    path('profile/change-password/', views.change_password_view, name='change_password'),
]
