from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib import messages
from .forms import UserRegistrationForm, DoctorReservationForm, PatientProfileForm
from .models import User, Doctor, Patient
from Reservations.models import Reservations
from Wallet.models import Wallet
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

    allow_doctor = getattr(settings, 'ALLOW_DOCTOR_REGISTRATION', True)
    allow_patient = getattr(settings, 'ALLOW_PATIENT_REGISTRATION', True)

    if not allow_doctor and not allow_patient:
        return render(request, 'accounts/register.html', {
            'form': None,
            'allow_doctor': allow_doctor,
            'allow_patient': allow_patient
        })

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            role = form.cleaned_data['role']

            if role == User.Role.DOCTOR and not allow_doctor:
                messages.error(
                    request, "Doctor registration is currently closed.")
                return redirect('register')

            if role == User.Role.PATIENT and not allow_patient:
                messages.error(
                    request, "Patient registration is currently closed.")
                return redirect('register')

            user = form.save(commit=False)
            user.role = role

            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']

            user.save()

            wallet = Wallet.objects.create(balance=0)

            if role == User.Role.DOCTOR:
                specialty = form.cleaned_data['specialty']
                medical_code = f"DR-{user.id:04d}"

                Doctor.objects.create(
                    user=user,
                    specialty=specialty,
                    wallet=wallet,
                    medical_code=medical_code,
                    monthly_reservation_capacity=50,
                )

            else:
                Patient.objects.create(user=user, wallet=wallet)

            messages.success(
                request, "Registration successful! You can now log in.")
            return redirect('login')

        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = UserRegistrationForm()

    if not allow_doctor:
        form.fields['role'].choices = [(User.Role.PATIENT, "Patient")]

    if not allow_patient:
        form.fields['role'].choices = [(User.Role.DOCTOR, "Doctor")]

    return render(request, 'accounts/register.html', {
        'form': form,
        'allow_doctor': allow_doctor,
        'allow_patient': allow_patient,
    })


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

    reservations = Reservations.objects.filter(
        doctor=doctor_instance).order_by('date', 'created_at')
    context = {
        'doctor': doctor_instance,
        'reservations': reservations,
    }
    return render(request, 'accounts/doctor_dashboard.html', context)


def doctors_list(request):
    doctors = Doctor.objects.filter(
        user__active=True).select_related('user', 'specialty')

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


def doctor_details(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id, user__active=True)
    can_book = request.user.is_authenticated and request.user.role == 'patient'
    return render(request, 'doctors/detail.html', {'doctor': doctor, 'can_book': can_book})


@login_required
def doctor_reservation(request, doctor_id):
    doctor = get_object_or_404(Doctor, user__id=doctor_id)

    if request.user.role != User.Role.PATIENT:
        return render(request, 'error.html', {'message': 'Only patients can book appointments.'})

    if request.method == "POST":
        form = DoctorReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.doctor = doctor
            reservation.patient = request.user.patient
            reservation.status = Reservations.Status.WAITING
            reservation.save()
            messages.success(
                request,
                f"Your appointment with Dr. {doctor.user.get_full_name()} has been booked successfully."
            )
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = DoctorReservationForm()

    return render(request, 'booking/booking.html', {
        'form': form,
        'doctor': doctor,
    })


def edit_pateint_profile(request):
    if request.user.role != User.Role.PATIENT:
        return render(request, 'error.html', {'message': 'Access denied'})

    patient = request.user.patient

    if request.method == 'POST':
        form = PatientProfileForm(
            request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('patient_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PatientProfileForm(instance=patient)

    return render(request, 'accounts/edit_patient_profile.html', {'form': form})


def add_patient_specialty(request):
    specialties = Specialty.objects.all()
    if request.method == 'POST':
        specialty_id = request.POST.get('specialty')
        specialty = get_object_or_404(Specialty, id=specialty_id)
        patient = request.user.patient
        patient.specialty = specialty
        patient.save()
        messages.success(request, "Specialty added successfully.")
        return redirect('patient_dashboard')
    return render(request, 'accounts/add_patient_specialty.html', {'specialties': specialties})


def patient_request_reservation(request):
    if request.user.role != User.Role.PATIENT:
        return render(request, 'error.html', {'message': 'Access denied'})

    patient = request.user.patient
    reservations = Reservations.objects.filter(
        patient=patient).order_by('-created_at')

    return render(request, 'accounts/patient_reservations.html', {'reservations': reservations})
