from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from employees.forms import RegistrationForm

class RegistrationTests(TestCase):
    def test_registration_form_invalid_admin_code(self):
        # Test that registration form fails validation when admin code is wrong
        data = {
            'username': 'testadmin',
            'first_name': 'Test',
            'last_name': 'Admin',
            'email': 'test@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'admin_code': 'wrongcode'
        }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('admin_code', form.errors)
        self.assertEqual(form.errors['admin_code'], ['Invalid admin registration code.'])

    def test_registration_form_correct_admin_code(self):
        # Test that registration form passes validation when admin code is correct
        data = {
            'username': 'testadmin',
            'first_name': 'Test',
            'last_name': 'Admin',
            'email': 'test@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'admin_code': 'admin123'
        }
        form = RegistrationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_register_view_invalid_admin_code(self):
        # Test that posting to register view with incorrect code fails and does not create user
        response = self.client.post(reverse('register'), {
            'username': 'testadmin2',
            'first_name': 'Test',
            'last_name': 'Admin',
            'email': 'test2@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'admin_code': 'wrongcode'
        })
        self.assertEqual(response.status_code, 200) # Re-renders register page
        self.assertFalse(User.objects.filter(username='testadmin2').exists())

    def test_register_view_correct_admin_code(self):
        # Test that posting to register view with correct code redirects and creates user
        response = self.client.post(reverse('register'), {
            'username': 'testadmin3',
            'first_name': 'Test',
            'last_name': 'Admin',
            'email': 'test3@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'admin_code': 'admin123'
        })
        self.assertEqual(response.status_code, 302) # Redirects to login
        self.assertTrue(User.objects.filter(username='testadmin3').exists())
