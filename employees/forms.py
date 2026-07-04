from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Employee, Department, UserProfile
import re


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))
    admin_code = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Enter admin registration code'}), label="Admin Code")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'

    def clean_admin_code(self):
        admin_code = self.cleaned_data.get('admin_code')
        if admin_code != 'admin123':
            raise forms.ValidationError("Invalid admin registration code.")
        return admin_code


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'gender',
            'date_of_birth', 'department', 'designation', 'salary',
            'joining_date', 'address', 'profile_photo', 'status'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter designation'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter salary', 'step': '0.01'}),
            'joining_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter address'}),
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^\+?[\d\s\-]{7,15}$', phone):
            raise forms.ValidationError("Enter a valid phone number.")
        return phone

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary is not None and salary < 0:
            raise forms.ValidationError("Salary cannot be negative.")
        return salary

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Employee.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter department name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
        }


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ['phone', 'photo']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
