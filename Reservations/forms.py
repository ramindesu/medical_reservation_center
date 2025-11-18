from django import forms
from Reservations.models import Reservations

class PatientReservationForm(forms.ModelForm):
    class Meta:
        model = Reservations
        fields = ['doctor', 'date', 'service']
        
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'service': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service'}),
        }

        labels = {
            'doctor': 'Doctor',
            'date': 'Appointment Date',
            'service': 'Service Needed',
        }
