from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from Medical_Archive.models import Specialty
from Reservations.models import Reservations

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from Medical_Archive.models import Specialty
from Reservations.models import Reservations

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[
            (User.Role.PATIENT, "Patient"),
            (User.Role.DOCTOR, "Doctor"),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    specialty = forms.ModelChoiceField(
        queryset=Specialty.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    address = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'phone', 'address', 'avatar', 'password1', 'password2',
            'role', 'specialty',
        ]

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        specialty = cleaned_data.get("specialty")

        if role == User.Role.DOCTOR and not specialty:
            self.add_error("specialty", "Please select a specialty for doctor.")

        return cleaned_data




class DoctorReservationForm(forms.ModelForm):
    class Meta:
        model = Reservations
        fields = ['date', 'service']
        
        widgets = {
            
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control glass-input'}),
            'service': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Service type...'}),
        }
        labels = {
            'date': 'Date',
            'service': 'Service',
        }