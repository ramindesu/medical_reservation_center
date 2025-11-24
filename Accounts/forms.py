from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Doctor, Patient
from Medical_Archive.models import Specialty
from Reservations.models import Reservations, FeedBack
from Wallet.models import Wallet
from Configs.models import Blacklist, ReservationBlock

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

    avatar = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'class': 'form-control'}))

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

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DoctorProfileForm(forms.ModelForm):

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
    address = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control glass-input',
                                  'placeholder': 'Enter new address...'
                              }))
    specialty = forms.ModelChoiceField(
        queryset=Specialty.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select glass-input'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'phone', 'address', 'specialty']
        # widgets = {
        #     'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control'}),
        #     'phone': forms.TextInput(attrs={'class': 'form-control'}),
        #     'address': forms.TextInput(attrs={'class': 'form-control'}),
        # }


class PatientReservationForm(forms.ModelForm):
    class Meta:
        model = Reservations
        fields = ['doctor', 'date', 'service']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'service': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
        }
# ------------------------
class AdminUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    specialty = forms.ModelChoiceField(
        queryset=Specialty.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    monthly_appointment_limit = forms.IntegerField(
        required=False,
        initial=5,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    monthly_reservation_capacity = forms.IntegerField(
        required=False,
        initial=50,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'phone', 'address', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        specialty = cleaned_data.get('specialty')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        if role == User.Role.DOCTOR and not specialty:
            raise forms.ValidationError("Specialty is required for doctors")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)

        if commit:
            user.save()
            wallet = Wallet.objects.create(balance=0)

            role = self.cleaned_data.get('role')
            if role == User.Role.PATIENT:
                monthly_limit = self.cleaned_data.get(
                    'monthly_appointment_limit', 5)
                Patient.objects.create(
                    user=user, wallet=wallet, monthly_appointment_limit=monthly_limit)
            elif role == User.Role.DOCTOR:
                specialty = self.cleaned_data.get('specialty')
                monthly_capacity = self.cleaned_data.get(
                    'monthly_reservation_capacity', 50)
                medical_code = f"DR-{user.id:04d}"
                Doctor.objects.create(
                    user=user,
                    specialty=specialty,
                    wallet=wallet,
                    medical_code=medical_code,
                    monthly_reservation_capacity=monthly_capacity
                )

        return user

# -------------------


class AdminUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'phone', 'address', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_active': 'Active',
        }


class PatientEditForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['monthly_appointment_limit']
        widgets = {
            'monthly_appointment_limit': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'monthly_appointment_limit': 'monthly limit reservation no',
        }


class DoctorEditForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialty', 'monthly_reservation_capacity', 'medical_code']
        widgets = {
            'specialty': forms.Select(attrs={'class': 'form-select'}),
            'monthly_reservation_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'medical_code': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'specialty': 'specialty',
            'monthly_reservation_capacity': 'reservvation capacity',
            'medical_code': 'medical code',
        }


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
# -----------------------------------------------------------

class BlacklistForm(forms.ModelForm):
    class Meta:
        model = Blacklist
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Reason for blocking'}),
        }
        labels = {
            'reason': 'Reason',
        }



class BlockReservationForm(forms.ModelForm):
    class Meta:
        model = ReservationBlock
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Reason for blocking this request'}),
        }
        labels = {
            'reason': 'Reason',
        }
