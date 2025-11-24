from django.shortcuts import get_object_or_404, redirect
from itertools import count
import re
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib import messages
from .forms import UserRegistrationForm, DoctorReservationForm, AdminUserCreationForm, AdminUserEditForm, FeedBackForm
from .models import User, Doctor, Patient
from Reservations.models import Reservations
from Wallet.models import Wallet
from Medical_Archive.models import Specialty
from django.db.models import Q
from datetime import date 
from Reservations.models import Reservations
from .forms import PatientProfileForm, PatientReservationForm, DoctorProfileForm
from .forms import PatientProfileForm, PatientReservationForm, DoctorProfileForm, BlacklistForm, BlockReservationForm, ReservationBlock
from datetime import datetime
from django.urls import reverse_lazy
from Reservations.models import FeedBack
from django.db.models import Avg, Count
from django.utils import timezone

from Configs.models import Blacklist



class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        if not form.get_user().is_active:
            form.add_error(
                None, "Your account is deactivated. Please contact admin.")
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return reverse('admin_dashboard')
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
                    avatar=request.FILES.get('avatar')
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
    patient = request.user.patient
    max_reservations_per_month = 5
    today = date.today()
    count_reservations = Reservations.objects.filter(
        patient=patient,
        created_at__year=today.year,
        created_at__month=today.month
    ).count()
    if count_reservations >= max_reservations_per_month:
        messages.error(
            request,
            f"You have reached the maximum number of {max_reservations_per_month} reservations for this month."
        )
        return redirect('patient_dashboard')

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
            return redirect('patient_dashboard')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = DoctorReservationForm()

    return render(request, 'booking/booking.html', {
        'form': form,
        'doctor': doctor,
    })


@login_required
def edit_doctor_profile(request):
    if request.user.role != User.Role.DOCTOR:
        return render(request, 'error.html', {'message': 'Access denied'})

    user = request.user

    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            user.first_name = form.cleaned_data.get(
                'first_name', user.first_name)
            user.last_name = form.cleaned_data.get('last_name', user.last_name)
            user.email = form.cleaned_data.get('email', user.email)
            user.phone = form.cleaned_data.get('phone', user.phone)
            user.address = form.cleaned_data.get('address', user.address)
            user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('doctor_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DoctorProfileForm(instance=user)

    return render(request, 'accounts/edit_doctor_profile.html', {'form': form})


# @login_required
# def request_appointment(request):
#     patient = Patient.objects.get(user=request.user)
#     now = datetime.now()
#     current_month = now.month
#     current_year = now.year
#     confirmed_count = Reservations.objects.filter( patient=patient, date__month=current_month,date__year=current_year,status='approved').count()

#     if request.method == 'POST':
#         form = PatientReservationForm(request.POST)
#         if form.is_valid():
#             if confirmed_count >= patient.monthly_appointment_limit:
#                 messages.error(request, "You have reached your monthly appointment limit.")
#             else:
#                 reservation = form.save(commit=False)
#                 reservation.patient = patient
#                 reservation.status = 'pending'
#                 reservation.save()
#                 messages.success(request, "Your appointment request has been submitted.")
#                 return redirect('patient_dashboard')
#     else:
#         form = PatientReservationForm()

#     return render(request, 'reservations/request_appointment.html', {'form': form})

@login_required
def edit_patient_profile(request):
    if request.user.role != User.Role.PATIENT:
        return render(request, 'error.html', {'message': 'Access denied'})

    user = request.user

    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('patient_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PatientProfileForm(instance=user)

    return render(request, 'accounts/edit_patient_profile.html', {'form': form})


@login_required
def full_appointment_history(request):

    if request.user.role != User.Role.PATIENT:
        return render(request, 'error.html', {'message': 'Access denied'})

    reservations = Reservations.objects.select_related(
        "doctor__user",
        "patient__user"
    ).prefetch_related("feedback_set")

    doctors_rating = (
        FeedBack.objects
        .values(
            "doctor_id",
            "doctor__user__first_name",
            "doctor__user__last_name",
            "doctor__specialty__title"
        )
        .annotate(
            avg_rating=Avg("rating"),
            total_feedback=Count("id")
        )
    )

    top_doctors = [d for d in doctors_rating if d["avg_rating"] >= 5]
    low_doctors = [d for d in doctors_rating if d["avg_rating"] < 5]

    top_doctors = sorted(top_doctors, key=lambda x: -x["avg_rating"])
    low_doctors = sorted(low_doctors, key=lambda x: x["avg_rating"])

    return render(request, "accounts/full_appointment_history.html", {
        "reservations": reservations,
        "top_doctors": top_doctors,
        "low_doctors": low_doctors,
    })


@login_required
def add_feedback(request, reservation_id):
    reservation = get_object_or_404(Reservations, id=reservation_id)

    if request.user.role != User.Role.PATIENT:
        return render(request, 'error.html', {'message': 'Access denied'})
    if reservation.patient.user != request.user:
        return render(request, 'error.html', {'message': 'You can only add feedback for your own reservations.'})
    if reservation.status != Reservations.Status.APPROVED:
        return render(request, 'error.html', {'message': 'Feedback can only be added for approved reservations.'})

    if request.method == 'POST':
        form = FeedBackForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']
            feedback = form.save(commit=False)
            feedback.reservation = reservation
            feedback.doctor = reservation.doctor
            feedback.patient = reservation.patient
            feedback.rating = rating
            feedback.comment = comment
            feedback.save()

        messages.success(request, "Thank you for your feedback!")
        return redirect('patient_reservations')

    return render(request, 'accounts/add_feedback.html', {'reservation': reservation, 'form': FeedBackForm()})

# ---------------------------


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Login required")

        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        if request.user.role != User.Role.ADMIN:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Access denied - Admin only")

        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@admin_required
def admin_dashboard(request):
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    total_appointments = Reservations.objects.count()

    from django.utils import timezone
    today_appointments = Reservations.objects.filter(
        date=timezone.now().date()).count()

    recent_users = User.objects.all().order_by('-date_joined')[:5]

    recent_appointments = Reservations.objects.all().order_by(
        '-created_at')[:5]

    context = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'today_appointments': today_appointments,
        'users': recent_users,
        'appointments': recent_appointments,
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
@admin_required
def admin_manage_users(request, user_type):
    if user_type == 'patients':
        users = Patient.objects.all().select_related('user')
        template = 'admin/manage_patients.html'
        title = 'manage patients'
    elif user_type == 'doctors':
        users = Doctor.objects.all().select_related('user', 'specialty')
        template = 'admin/manage_doctors.html'
        title = 'manage doctors'
    else:
        users = User.objects.all()
        template = 'admin/manage_users.html'
        title = 'manage all users'

    search_query = request.GET.get('search')
    if search_query:
        if user_type == 'patients':
            users = users.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(user__email__icontains=search_query) |
                Q(user__phone__icontains=search_query)
            )
        elif user_type == 'doctors':
            users = users.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(user__email__icontains=search_query) |
                Q(medical_code__icontains=search_query) |
                Q(specialty__title__icontains=search_query)
            )
        else:
            users = users.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(phone__icontains=search_query) |
                Q(username__icontains=search_query)
            )

    context = {
        'users': users,
        'user_type': user_type,
        'title': title,
        'search_query': search_query or '',
    }
    return render(request, template, context)


@login_required
@admin_required
def admin_add_user(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, f"User {user.username} created successfully!")
            return redirect('admin_manage_users', user_type='all')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AdminUserCreationForm()

    return render(request, 'admin/add_user.html', {'form': form})


@login_required
@admin_required
def admin_edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"user information  {user.username} updated successfully.")
            return redirect('admin_manage_users', user_type='all')
        else:
            messages.error(request, "please correct errors")
    else:
        form = AdminUserEditForm(instance=user)

    context = {
        'form': form,
        'user': user,
        'is_patient': hasattr(user, 'patient'),
        'is_doctor': hasattr(user, 'doctor'),
    }
    return render(request, 'admin/edit_user.html', context)


@login_required
@admin_required
def admin_manage_appointments(request):
    appointments = Reservations.objects.all().order_by('-created_at')

    urgent_requests = appointments.filter(status='waiting')

    from django.utils import timezone
    from datetime import timedelta 
    two_days_later = timezone.now().date() + timedelta(days=2)
    urgent_requests = appointments.filter(status='waiting' , date=two_days_later)

    tomorrow = timezone.now().date() + timedelta(days=1)
    expiring_appointments = appointments.filter(
        date=tomorrow, status='waiting').exclude(patient_id__in=blocked_patients)

    for appointment in appointments:
        if appointment.status == 'waiting' and appointment.patient_id in blocked_patients:
            appointment.status = 'blocked'

    context = {
        'appointments': appointments,
        'urgent_requests': urgent_requests,
        'expiring_appointments': expiring_appointments,
    }
    return render(request, 'admin/manage_appointments.html', context)


@login_required
def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Reservations, id=appointment_id)

    if request.method == "POST":
        appointment.status = Reservations.Status.APPROVED
        appointment.save()
        messages.success(
            request, f"Appointment with {appointment.patient.user.get_full_name} approved.")
        return redirect('manage_appointments')

    return redirect('manage_appointments')


@login_required
def reject_appointment(request, appointment_id):
    appointment = get_object_or_404(Reservations, id=appointment_id)

    if request.method == "POST":
        appointment.status = Reservations.Status.REJECTED
        appointment.save()
        messages.success(
            request, f"Appointment with {appointment.patient.user.get_full_name} rejected.")
        return redirect('manage_appointments')

    return redirect('manage_appointments')


@login_required
def view_appointment(request, appointment_id):
    appointment = get_object_or_404(Reservations, id=appointment_id)
    return render(request, 'appointments/view_appointment.html', {
        'appointment': appointment
    })


@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Reservations, id=appointment_id)

    if request.method == "POST":
        form = DoctorReservationForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment updated successfully.")
            return redirect('manage_appointments')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DoctorReservationForm(instance=appointment)

    return render(request, 'appointments/edit_appointment.html', {
        'form': form,
        'appointment': appointment
    })
# --------------------------------------------------------------------------

@login_required
def doctor_requests(request):
    if request.user.role != User.Role.DOCTOR:
        return render(request, 'error.html', {'message': 'Access denied'})

    doctor = request.user.doctor

    blacklisted_patients = Blacklist.objects.filter(
        doctor=doctor,
        active=True
    ).values_list("patient_id", flat=True)

    reservations = Reservations.objects.filter(
        doctor=doctor,
        status=Reservations.Status.WAITING
    ).exclude(patient_id__in=blacklisted_patients).order_by("date", "time")

    return render(request, "accounts/doctor_requests.html", {
        "doctor": doctor,
        "reservations": reservations,
        "BlacklistForm": BlacklistForm(),
    })



@login_required
def doctor_accept(request, reservation_id):
    reservation = get_object_or_404(Reservations, id=reservation_id)

    if request.user.role != User.Role.DOCTOR:
        return render(request, "error.html", {"message": "Access denied"})

    doctor = request.user.doctor

    reservation.status = Reservations.Status.APPROVED
    reservation.doctor = doctor
    reservation.save()

 
    Reservations.objects.filter(
        date=reservation.date,
        time=reservation.time,
        doctor__specialty=doctor.specialty
    ).exclude(id=reservation.id).delete()

    messages.success(request, "Appointment approved successfully.")
    return redirect("doctor_requests")




@login_required
def doctor_reject(request, reservation_id):
    reservation = get_object_or_404(Reservations, id=reservation_id)

    if request.user.role != User.Role.DOCTOR:
        return render(request, "error.html", {"message": "Access denied"})

    reservation.status = Reservations.Status.REJECTED
    reservation.save()

    messages.success(request, "Appointment rejected.")
    return redirect("doctor_requests")


@login_required
def doctor_blacklist(request, reservation_id):
    reservation = get_object_or_404(Reservations, id=reservation_id)
    
    if request.user.role != User.Role.DOCTOR:
        messages.error(request, "Access denied")
        return redirect("doctor_requests")
    
    doctor = request.user.doctor
    patient = reservation.patient

    if request.method == "POST":
        form = BlacklistForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            bl, created = Blacklist.objects.get_or_create(
                doctor=doctor,
                patient=patient,
                defaults={'reason': reason, 'active': True}
            )
            if not created:
                bl.active = True
                bl.reason = reason
                bl.save()
            messages.success(request, f"{patient.user.get_full_name} has been blacklisted.")
            return redirect("doctor_requests")
    else:
        form = BlacklistForm()

    return render(request, "accounts/doctor_blacklist.html", {"form": form, "patient": patient})


@login_required
def doctor_block_request(request, reservation_id):
    reservation = get_object_or_404(Reservations, id=reservation_id)
    
    if request.method == 'POST':
        form = BlockReservationForm(request.POST)
        if form.is_valid():
            blocked_request, created = ReservationBlock.objects.get_or_create(
                reservation=reservation,
                defaults={'reason': form.cleaned_data['reason'], 'active': True}
            )
            if not created:
                blocked_request.active = True
                blocked_request.reason = form.cleaned_data['reason']
                blocked_request.save()
            messages.success(request, "Request has been blocked successfully.")
            return redirect('doctor_requests')
    else:
        form = BlockReservationForm()
    
    return render(request, 'accounts/block_request.html', {'form': form})




# -----------RAMIN------------


def patinet_list(request):
    if request.user.role != User.Role.DOCTOR:
        return render(request, 'error.html', {'message': 'Access denied'})
    
    doctor = request.user.doctor  
    now = timezone.now()
    
    appointments = Reservations.objects.filter(
        doctor=doctor,
        status=Reservations.Status.APPROVED,
        date__lt=now
    )

    return render(request, 'doctors/patient-list.html', {'appointments': appointments})