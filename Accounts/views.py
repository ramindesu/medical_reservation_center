from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import User
from Reservations.models import Reservations



class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.role == User.Role.DOCTOR:
            return reverse('doctor_dashboard')
        elif user.role == User.Role.PATIENT:
            return reverse('patient_dashboard')
        return '/'


def register(request):
    role = 'patient'

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            specialty = form.cleaned_data.get('specialty')

            user = form.save(commit=False)
            user.role = role
            if role == 'doctor':
                if not specialty:
                    messages.error(request, "Please enter your specialty.")
                    return render(request, 'accounts/register.html', {'form': form, 'role': role})
                user.specialty = specialty
            user.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form, 'role': role})



def home_redirect(request):
    if request.user.is_authenticated:
        if request.user.role == User.Role.DOCTOR:
            return redirect('doctor_dashboard')
        elif request.user.role == User.Role.PATIENT:
            return redirect('patient_dashboard')
    return redirect('login')



@login_required
def patient_dashboard(request):
    if request.user.role != 'patient':
        return render(request, 'error.html', {'message': 'Access denied'})
    
    context = {
        'user': request.user,
    }
    return render(request, 'accounts/patient_dashboard.html', context)




@login_required
def doctor_dashboard(request):
    if not hasattr(request.user, 'doctor'):
        return render(request, 'error.html', {'message': 'Access denied'})
    reservations = Reservations.objects.filter(doctor=request.user.doctor).order_by('date', 'created_at')
    return render(request, 'accounts/doctor_dashboard.html', {'reservations': reservations})
