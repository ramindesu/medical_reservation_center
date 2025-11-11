from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class PatientRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'address', 'password1', 'password2']

class DoctorRegistrationForm(UserCreationForm):
    specialty = forms.CharField(max_length=100) 

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'address', 'password1', 'password2']
