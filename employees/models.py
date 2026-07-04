from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Employee(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    designation = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    joining_date = models.DateField()
    address = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='employee_photos/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def employee_id(self):
        return f"EMP{self.id:03d}"

    class Meta:
        ordering = ['-id']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"
