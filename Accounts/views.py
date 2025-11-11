from django.conf import settings
from django.shortcuts import render, redirect
from .forms import PatientRegistrationForm, DoctorRegistrationForm
from django.contrib.auth.decorators import login_required
from Reservations.models import Reservations
from django.contrib.auth.views import LoginView
from django.urls import reverse
from Accounts.models import Patient
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Patient.objects.create(user=user, wallet=None)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.role == 'doctor':
            return reverse('doctor_dashboard')
        elif user.role == 'patient':
            return reverse('patient_dashboard')
        else:
            return reverse('login')  



def login_redirect(request):
    if request.user.role == 'doctor':
        return redirect('/doctor/dashboard/')
    elif request.user.role == 'patient':
        return redirect('/patient/dashboard/')
    return redirect('/')


@login_required
def patient_dashboard(request):
    if not hasattr(request.user, 'patient'):
        return render(request, 'error.html', {'message': 'Access denied'})
    
    reservations = Reservations.objects.filter(patient=request.user.patient).order_by('date', 'created_at')
    return render(request, 'patient-dashboard.html', {'reservations': reservations})

@login_required
def doctor_dashboard(request):
    if not hasattr(request.user, 'doctor'):
        return render(request, 'error.html', {'message': 'Access denied'})
    
    reservations = Reservations.objects.filter(doctor=request.user.doctor).order_by('date', 'created_at')
    return render(request, 'doctor-dashboard.html', {'reservations': reservations})



def home_redirect(request):
    if request.user.is_authenticated:
        if request.user.role == 'doctor':
            return redirect('doctor_dashboard')  
        elif request.user.role == 'patient':
            return redirect('patient_dashboard')  
    else:
        return redirect('login')



def patient_register_view(request):
    allow_registration = getattr(settings, 'ALLOW_PATIENT_REGISTRATION', True)
    form = PatientRegistrationForm()
    if request.method == 'POST' and allow_registration:
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'accounts/register.html', {'form': form, 'allow_registration': allow_registration})



def doctor_register_view(request):
    allow_registration = getattr(settings, 'ALLOW_DOCTOR_REGISTRATION', True)
    form = DoctorRegistrationForm()
    if request.method == 'POST' and allow_registration:
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'accounts/register.html', {'form': form, 'allow_registration': allow_registration})
