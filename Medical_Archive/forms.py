from django import forms
from Reservations.models import Reservations

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservations
        fields = ['date', 'service']
        
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'service': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Service type...'
            }),
        }
