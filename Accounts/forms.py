from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Role")
    specialty = forms.CharField(max_length=100, required=False, label="Specialty (for doctors)")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'address', 'password1', 'password2', 'role', 'specialty']
