from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Patient, Doctor


class PatientRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Patient
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'address', 'password1', 'password2']




class DoctorRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)
    medical_code = forms.CharField(max_length=30)
    specialty = forms.ModelChoiceField(queryset=None)  
    monthly_reservation_capacity = forms.IntegerField(initial=50)

    class Meta:
        model = Doctor
        fields = [
            'username', 'email', 'first_name', 'last_name', 'phone', 'address',
            'medical_code', 'specialty', 'monthly_reservation_capacity',
            'password1', 'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from Medical_Archive.models import Specialty
        self.fields['specialty'].queryset = Specialty.objects.all()
