from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import User, Doctor, Patient
from Reservations.models import Reservations
from Medical_Archive.models import Specialty
from django.db.models import Q


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
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data['role']
            user.role = role
            if role == User.Role.PATIENT:
                user.address = ""
            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']
            user.save()

            
            wallet = Wallet.objects.create(balance=0)

            if role == User.Role.DOCTOR:
                specialty = form.cleaned_data.get('specialty')
                medical_code = f"DR-{user.id:04d}"
                Doctor.objects.create(
                    user=user,
                    specialty=specialty,
                    wallet=wallet,
                    avatar=user.avatar,
                    medical_code=medical_code,
                    monthly_reservation_capacity=50
                )
            else: 
                Patient.objects.create(user=user, wallet=wallet)

            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
        else:
           
            print(form.errors)
            messages.error(request, "Please fix the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def home_redirect(request):
    if request.user.is_authenticated:
        if request.user.role == User.Role.DOCTOR:
            return redirect('doctor_dashboard')
        elif request.user.role == User.Role.PATIENT:
            return redirect('patient_dashboard')
    return redirect('login')


@login_required
def patient_dashboard(request):
    if request.user.role != User.Role.PATIENT:
        return render(request, 'error.html', {'message': 'Access denied'})
    
    context = {'user': request.user}
    return render(request, 'accounts/patient_dashboard.html', context)


@login_required
def doctor_dashboard(request):
    try:
        doctor_instance = request.user.doctor
    except Doctor.DoesNotExist:
        return render(request, 'accounts/error.html', {'message': 'No doctor profile found.'})

    reservations = Reservations.objects.filter(doctor=doctor_instance).order_by('date', 'created_at')
    context = {
        'doctor': doctor_instance,
        'reservations': reservations,
    }
    return render(request, 'accounts/doctor_dashboard.html', context)


def doctors_list(request):
    doctors = Doctor.objects.filter(user__active=True).select_related('user', 'specialty')
    # doctors = Doctor.objects.filter(user__active=True).exclude(id__isnull=True).select_related('user', 'specialty')

    specialty_filter = request.GET.get('specialty')
    if specialty_filter:
        doctors = doctors.filter(specialty_id=specialty_filter)

    search_query = request.GET.get('search')
    if search_query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(specialty__title__icontains=search_query)
        )

    specialties = Specialty.objects.all()
    return render(request, 'doctors/list.html', {
        'doctors': doctors,
        'specialties': specialties
    })


def booking_page(request, doctor_id):
    if not request.user.is_authenticated or request.user.role != User.Role.PATIENT:
        return render(request, 'error.html', {'message': 'Only patients can book appointments'})

    doctor = get_object_or_404(Doctor, pk=doctor_id, user__active=True)

    if request.method == 'POST':
        date = request.POST.get('date')
        service = request.POST.get('service')

        Reservations.objects.create(
            doctor=doctor,
            patient=request.user.patient,
            date=date,
            service=service,
            status=Reservations.Status.WAITING
        )
        messages.success(request, "Appointment booked successfully!")
        return redirect('patient_dashboard')

    return render(request, 'booking/booking.html', {'doctor': doctor, 'doctor_id': doctor_id})
