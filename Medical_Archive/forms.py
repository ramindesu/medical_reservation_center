from django import forms
from Reservations.models import Reservations

class DoctorReservationForm(forms.ModelForm):
    class Meta:
        model = Reservations
        fields = ['patient', 'date', 'service']
        
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control glass-input'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control glass-input'}),
            'service': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Service type...'}),
        }
        labels = {
            'patient': 'Patient',
            'date': 'Date',
            'service': 'Service',
        }
