from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from Medical_Archive.models import Specialty
from Reservations.models import FeedBack, Reservations


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
    
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'phone', 'address', 'password1', 'password2',
            'role', 'specialty',
        ]

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        specialty = cleaned_data.get("specialty")

        if role == User.Role.DOCTOR and not specialty:
            self.add_error(
                "specialty", "Please select a specialty for doctor.")

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


class PatientProfileForm(forms.ModelForm):

    first_name = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control glass-input',
                                     'placeholder': 'Enter new first name...'
                                 }))

    last_name = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control glass-input',
                                    'placeholder': 'Enter new last name...'
                                }))

    email = forms.EmailField(required=False,
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control glass-input',
                                 'placeholder': 'Enter new email...'
                             }))

    phone = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={
                                'class': 'form-control glass-input',
                                'placeholder': 'Enter new phone number...'
                            }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone',]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            user_id = self.instance.id
            if User.objects.exclude(id=user_id).filter(email=email).exists():
                raise forms.ValidationError(
                    "This email is already taken")
        return email


class FeedBackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ['rating', 'comment']

        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control glass-input', 'min': '0', 'max': '10'}),
            'comment': forms.Textarea(attrs={'class': 'form-control glass-input', 'placeholder': 'Your feedback...'}),
        }
        labels = {
            'rating': 'Rating (0-10)',
            'comment': 'Comment',
        }
