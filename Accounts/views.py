from django.conf import settings
from django.shortcuts import render, redirect
from .forms import PatientRegistrationForm, DoctorRegistrationForm
from django.contrib.auth.decorators import login_required
from Reservations.models import Reservations


@login_required
def patient_dashboard(request):
    if not hasattr(request.user, 'patient'):
        return render(request, 'error.html', {'message': 'Access denied'})
    
    reservations = Reservations.objects.filter(patient=request.user.patient).order_by('date', 'created_at')
    return render(request, 'dashboard_patient.html', {'reservations': reservations})

@login_required
def doctor_dashboard(request):
    if not hasattr(request.user, 'doctor'):
        return render(request, 'error.html', {'message': 'Access denied'})
    
    reservations = Reservations.objects.filter(doctor=request.user.doctor).order_by('date', 'created_at')
    return render(request, 'dashboard_doctor.html', {'reservations': reservations})



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
