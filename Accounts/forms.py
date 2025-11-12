from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from Medical_Archive.models import Specialty

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
            raise forms.ValidationError("Please select a specialty for doctor.")
        return cleaned_data
