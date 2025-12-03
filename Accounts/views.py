from django.shortcuts import get_object_or_404, redirect, HttpResponse
from itertools import count
import re
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib import messages
from .forms import IncreaseCapacityForm, UserRegistrationForm, DoctorReservationForm, AdminUserCreationForm, AdminUserEditForm, FeedBackForm
from .models import User, Doctor, Patient , CapacityIncreaseRequest
from Reservations.models import Reservations
from Wallet.models import Wallet
from Medical_Archive.models import Specialty
from django.db.models import Q , Sum 
from datetime import date , datetime
from Reservations.models import Reservations
from .forms import PatientProfileForm, PatientReservationForm, DoctorProfileForm
from .forms import PatientProfileForm, PatientReservationForm, DoctorProfileForm, BlacklistForm, BlockReservationForm, ReservationBlock
from datetime import datetime
from django.urls import reverse_lazy
from Reservations.models import FeedBack
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta
from Configs.models import Blacklist, Config
from django import template

from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect('home')


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


# @login_required
# def doctor_dashboard(request):
#     try:
#         doctor_instance = request.user.doctor
#     except Doctor.DoesNotExist:
#         return render(request, 'accounts/error.html', {'message': 'No doctor profile found.'})
#     user = request.user
#     reservations = Reservations.objects.filter(
#         doctor=doctor_instance, status=Reservations.Status.APPROVED
#     ).select_related("patient__user").order_by('date', 'created_at')
#     context = {
#         'doctor': doctor_instance,
#         'user': user,
#         'reservations': reservations,
#     }
#     return render(request, 'accounts/doctor_dashboard.html', context)


@login_required
def doctor_dashboard(request):
    try:
        doctor_instance = request.user.doctor
    except Doctor.DoesNotExist:
        return render(request, 'accounts/error.html', {'message': 'No doctor profile found.'})
    
    now = timezone.now()
    current_month = now.month
    current_year = now.year
    
    current_reservations = Reservations.objects.filter(
        doctor=doctor_instance,
        status=Reservations.Status.APPROVED,
        date__month=current_month,
        date__year=current_year
    ).count()
    
    base_capacity = doctor_instance.monthly_reservation_capacity
    
    approved_requests = CapacityIncreaseRequest.objects.filter(
        doctor=doctor_instance,
        status='approved',
        created_at__month=current_month,
        created_at__year=current_year
    )
    
    increase_amount = 0
    has_active_approved_request = False
    
    if approved_requests.exists():
        has_active_approved_request = True
        
        aggregation = approved_requests.aggregate(
            total_requested=Sum('requested_capacity'),
            total_current=Sum('current_capacity'),

        )
        
        total_requested = aggregation['total_requested'] or 0
        total_current = aggregation['total_current'] or 0

        increase_amount = total_requested - total_current

    total_capacity = base_capacity + increase_amount

    available_capacity = total_capacity - current_reservations
    if available_capacity < 0:
        available_capacity = 0

    reservations = Reservations.objects.filter(
        doctor=doctor_instance, 
        status=Reservations.Status.APPROVED
    ).select_related("patient__user").order_by('date', 'created_at')

    is_capacity_full = current_reservations >= total_capacity
    is_low_capacity = 0 < available_capacity <= 2
    
   
    
    context = {
       'doctor': doctor_instance,
        'current_reservations': current_reservations,
        'available_capacity': available_capacity,
        'total_capacity': total_capacity,
        'base_capacity': base_capacity,
        'increase_amount': increase_amount,
        'has_approved_request': has_active_approved_request,
        'current_month': now.strftime("%B %Y"),
        'is_capacity_full': is_capacity_full,
        'is_low_capacity': is_low_capacity,

    }
    
    return render(request, 'accounts/doctor_dashboard.html', context)
# ----------------

def doctors_list(request):
    doctors = Doctor.objects.filter(
        user__active=True).select_related('user', 'specialty')
    
    doctors = doctors.annotate(
        avg_rating=Avg('feedback__rating'),
     )

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
    patient = request.user.patient

    if Blacklist.objects.filter(doctor=doctor, patient=patient, active=True).exists():
        messages.error(
            request, "You are blocked by this doctor. You cannot book an appointment.")
        return redirect('patient_dashboard')

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
    avg_rating = FeedBack.objects.filter(doctor=doctor).aggregate(
        avg_rating=Avg('rating')
        )['avg_rating']
    
    can_book = request.user.is_authenticated and request.user.role == 'patient'
    return render(request, 'doctors/detail.html', {'doctor': doctor, 'can_book': can_book , 'avg_rating': avg_rating})


@login_required
def doctor_reservation(request, doctor_id):
    doctor = get_object_or_404(Doctor, user__id=doctor_id)
    patient = request.user.patient

    if Blacklist.objects.filter(doctor=doctor, patient=patient, active=True).exists():
        messages.error(
            request, "You are blocked by this doctor. Reservation denied.")
        return redirect('patient_dashboard')

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
        form = PatientReservationForm(request.POST)
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
        form = PatientReservationForm()

    return render(request, 'booking/booking.html', {
        'form': form,
        'doctor': doctor,
    })


@login_required
def edit_doctor_profile(request):
    if request.user.role != User.Role.DOCTOR:
        return render(request, 'error.html', {'message': 'Access denied'})

    user = request.user
    doctor = request.user.doctor

    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, request.FILES, instance=doctor)

        if form.is_valid():

            form.save()

            user.first_name = form.cleaned_data.get(
                "first_name", user.first_name)
            user.last_name = form.cleaned_data.get("last_name", user.last_name)
            user.email = form.cleaned_data.get("email", user.email)
            user.phone = form.cleaned_data.get("phone", user.phone)
            user.address = form.cleaned_data.get("address", user.address)
            user.save()

            messages.success(request, "Profile updated successfully.")
            return redirect('doctor_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DoctorProfileForm(
            instance=doctor,
            initial={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.phone,
                "address": user.address,
                "specialty": doctor.specialty,
            }
        )

    return render(request, 'accounts/edit_doctor_profile.html', {
        'form': form,
        'doctor': doctor
    })


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
        return redirect('patient_dashboard')

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
    recent_capacity_requests = CapacityIncreaseRequest.objects.select_related('doctor__user').order_by('-created_at')[:5]

    context = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'today_appointments': today_appointments,
        'users': recent_users,
        'appointments': recent_appointments,
        'recent_capacity_requests': recent_capacity_requests,
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
    blocked_patients = set(Blacklist.objects.filter(
        active=True).values_list('patient_id', flat=True))

    from django.utils import timezone
    from datetime import timedelta
    two_days_later = timezone.now().date() + timedelta(days=2)
    urgent_requests = appointments.filter(
        date=two_days_later, status='waiting').exclude(patient_id__in=blocked_patients)

    from django.utils import timezone
    from datetime import timedelta
    tomorrow = timezone.now().date() + timedelta(days=1)
    expiring_appointments = appointments.filter(
        date=tomorrow, status='waiting').exclude(patient_id__in=blocked_patients)
    all_appointments = Reservations.objects.select_related(
        "doctor__user", "patient__user"
    ).order_by('-created_at')

    urgent_requests = []
    for appointment in all_appointments:
        is_blocked = Blacklist.objects.filter(
            doctor=appointment.doctor,
            patient=appointment.patient,
            active=True
        ).exists()

        if appointment.status == Reservations.Status.WAITING and not is_blocked:
            urgent_requests.append(appointment)

    context = {
        "appointments": all_appointments,
        "urgent_requests": urgent_requests,
    }

    return render(request, "admin/manage_appointments.html", context)


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
            if hasattr(request.user, 'doctor'):
                return redirect('doctor_appointments')
            else:
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

    today = timezone.now().date()
    two_days_later = today + timedelta(days=2)

    waiting_reservations = Reservations.objects.filter(
        doctor=doctor,
        status=Reservations.Status.WAITING
    ).exclude(patient_id__in=blacklisted_patients)

    urgent_requests = waiting_reservations.filter(
        date__lte=two_days_later
    ).order_by('date', 'time')

    normal_requests = waiting_reservations.filter(
        date__gt=two_days_later
    ).order_by('-created_at')

    reservations = list(urgent_requests) + list(normal_requests)

    return render(request, "accounts/doctor_requests.html", {
        "doctor": doctor,
        "reservations": reservations,
        "BlacklistForm": BlacklistForm(),
        "today": today,
        "two_days_later": two_days_later,
    })


@login_required
def doctor_accept(request, reservation_id):
    if request.user.role != User.Role.DOCTOR:
        return render(request, "error.html", {"message": "Access denied"})
    reservation = get_object_or_404(Reservations, id=reservation_id)
    doctor = request.user.doctor

    doctor.monthly_reservation_capacity -= 1
    doctor.save()

    reservation.status = Reservations.Status.APPROVED
    reservation.save()

    Reservations.objects.filter(
        date=reservation.date,
        # time=reservation.time,
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
    reason = request.POST.get("reason", "Blocked by doctor")

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
            messages.success(
                request, f"{patient.user.get_full_name} has been blacklisted.")
            return redirect("doctor_requests")
    else:
        form = BlacklistForm()

    return render(request, "accounts/doctor_blacklist.html", {"form": form, "patient": patient})


@login_required
def doctor_block_request(request, reservation_id):
    reservation = get_object_or_404(Reservations, id=reservation_id)

    if request.user.role != User.Role.DOCTOR:
        messages.error(request, "Access denied")
        return redirect("doctor_requests")

    if request.method == 'POST':
        form = BlockReservationForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']

            blocked_request, created = ReservationBlock.objects.update_or_create(
                reservation=reservation,
                defaults={
                    'reason': form.cleaned_data['reason'], 'active': True}
            )
            if not created:
                blocked_request.active = True
                blocked_request.reason = form.cleaned_data['reason']
                blocked_request.save()

            reservation.status = Reservations.Status.BLOCKED
            reservation.save()

            messages.success(request, "Request has been blocked successfully.")
            return redirect('doctor_requests')
    else:
        form = BlockReservationForm()

    return render(request, 'accounts/block_request.html', {'form': form})


# -----------RAMIN------------

@login_required
def patient_list(request):
    if request.user.role != User.Role.DOCTOR:
        return render(request, 'error.html', {'message': 'Access denied'})

    doctor = request.user.doctor
    today = timezone.now().date()

    doctor = request.user.doctor
    now = timezone.now()

    appointments = Reservations.objects.filter(
        doctor=doctor,
        status=Reservations.Status.APPROVED,
        date__lt=today,
    )

    return render(request, 'doctors/patient-list.html', {'appointments': appointments})

# ----------------------------


@login_required
def doctor_appointments(request):
    try:
        doctor_instance = request.user.doctor
    except Doctor.DoesNotExist:
        return render(request, 'accounts/error.html', {'message': 'No doctor profile found.'})
    user = request.user
    appointments = Reservations.objects.filter(
        doctor=doctor_instance,
        status=Reservations.Status.APPROVED
    ).select_related('patient__user').order_by('date', 'time')

    context = {
        'doctor': doctor_instance,
        'user': user,
        'appointments': appointments,
    }
    return render(request, 'accounts/doctor_appointments.html', context)


@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Reservations, id=appointment_id)
    if appointment.patient != request.user.patient:
        return render(request, 'error.html', {'message': 'Access denied'})
    if appointment.status != Reservations.Status.WAITING:
        messages.error(request, "Only waiting appointments can be canceled.")
        return redirect('patient_reservations')
    appointment.status = Reservations.Status.CANCELED
    appointment.save()
    messages.success(request, "Appointment canceled successfully.")
    return redirect('patient_dashboard')


@login_required
def create_followup_appointment(request, appointment_id):
    original_appointment = get_object_or_404(Reservations, id=appointment_id)

    if original_appointment.doctor != request.user.doctor:
        messages.error(
            request, "You can only create follow-up for your own appointments.")
        return redirect('doctor_appointments')

    if not original_appointment.is_in_progress:
        messages.error(
            request, "You can only create follow-up appointments for today's appointments.")
        return redirect('doctor_appointments')

    if request.method == "POST":
        date = request.POST.get('date')
        time = request.POST.get('time')
        service = request.POST.get(
            'service', f"Follow-up: {original_appointment.service}")

        if date and time:
            followup_date = datetime.strptime(date, '%Y-%m-%d').date()
            patient = original_appointment.patient
            monthly_reservations_count = Reservations.objects.filter(
                patient=patient,
                date__year=followup_date.year,
                date__month=followup_date.month,
                status__in=[Reservations.Status.APPROVED,
                            Reservations.Status.WAITING]
            ).count()

            max_reservations_per_month = 5

            if monthly_reservations_count >= max_reservations_per_month:
                messages.error(request,
                               f"This patient has reached the maximum number of {max_reservations_per_month} reservations for {followup_date.strftime('%B %Y')}.")

                context = {
                    'original_appointment': original_appointment,
                    'patient': patient,
                }
                return render(request, 'accounts/create_followup_appointment.html', context)
            else:
                Reservations.objects.create(
                    doctor=request.user.doctor,
                    patient=original_appointment.patient,
                    date=date,
                    time=time,
                    service=service,
                    status=Reservations.Status.APPROVED
                )
                messages.success(
                    request, f"Follow-up appointment created for {original_appointment.patient.user.get_full_name()}!")
                return redirect('doctor_appointments')
        else:
            messages.error(request, "Please fill in all required fields.")
            context = {
                'original_appointment': original_appointment,
                'patient': original_appointment.patient,
            }
            return render(request, 'accounts/create_followup_appointment.html', context)

    context = {
        'original_appointment': original_appointment,
        'patient': original_appointment.patient,
    }
    return render(request, 'accounts/create_followup_appointment.html', context)

    return render(request, 'doctors/patient-list.html', {'appointments': appointments},
                  )

# -------------------------------------------


@login_required
def doctor_add_feedback(request, reservation_id):
    reservation = get_object_or_404(Reservations, id=reservation_id)

    if request.user.role != User.Role.DOCTOR:
        return render(request, 'error.html', {'message': 'Access denied'})

    if reservation.doctor.user != request.user:
        return render(request, 'error.html', {
            'message': 'You can only add feedback for your own patients.'
        })

    if reservation.status != Reservations.Status.APPROVED:
        return render(request, 'error.html', {
            'message': 'Feedback can only be added for approved reservations.'
        })
    if reservation.date > timezone.now().date():
        return render(request, 'error.html', {
            'message': 'You can only add feedback after the visit date has passed.'
        })

    if request.method == 'POST':
        form = FeedBackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.reservation = reservation
            feedback.doctor = reservation.doctor
            feedback.patient = reservation.patient
            feedback.save()
            messages.success(request, "Feedback sent to patient successfully.")
            return redirect('doctor_dashboard')
    else:
        form = FeedBackForm()

    return render(
        request,
        'doctor_add_feedback.html',
        {'reservation': reservation, 'form': form}
    )


# @login_required
# def increase_capacity(request):
#     if request.user.role != User.Role.DOCTOR:
#         return render(request, 'error.html', {'message': 'Access denied'})

#     doctor = request.user.doctor

#     current_month = timezone.now().date().replace(day=1)
#     current_reservations = Reservations.objects.filter(
#         doctor=doctor,
#         status=Reservations.Status.APPROVED,
#         date__year=current_month.year,
#         date__month=current_month.month
#     ).count()

#     if current_reservations > doctor.monthly_reservation_capacity:
#         messages.warning(
#             request,
#             f"You still have {doctor.monthly_reservation_capacity - current_reservations} available slots. "
#             f"You can request capacity increase when you reach your current limit."
#         )
#         return redirect('doctor_dashboard')

#     if request.method == "POST":
#         form = IncreaseCapacityForm(request.POST)
#         if form.is_valid():
#             new_capacity = form.cleaned_data['new_capacity']
#             reason = request.POST.get('reason', '')

#             key = f"capacity_request_doctor_{doctor.user_id}"
#             Config.objects.update_or_create(
#                 key=key,
#                 defaults={
#                     "value": str(new_capacity),
#                     "description": f"Capacity: {doctor.monthly_reservation_capacity}→{new_capacity}. Reason: {reason}. Status: pending"
#                 }
#             )

#             messages.success(
#                 request,
#                 "Your capacity increase request has been submitted for admin approval."
#             )
#             return redirect("doctor_dashboard")
#     else:
#         form = IncreaseCapacityForm()

#     return render(request, "accounts/increase_capacity_form.html", {
#         "form": form,
#         "doctor": doctor,
#         "current_reservations": current_reservations
#     })


# ---------------------
# @login_required
# @admin_required
# def admin_manage_capacity_requests(request):
#     from Configs.models import Config

#     capacity_requests = []
#     config_requests = Config.objects.filter(
#         key__startswith="capacity_request_doctor_")

#     for config in config_requests:
#         try:

#             doctor_id = config.key.split('_')[-1]
#             doctor = Doctor.objects.get(user_id=doctor_id)

#             desc_parts = config.description.split('. ')
#             capacity_info = desc_parts[0].replace('Capacity: ', '')
#             current, requested = capacity_info.split('→')
#             reason = desc_parts[1].replace(
#                 'Reason: ', '') if len(desc_parts) > 1 else ""
#             status = desc_parts[2].replace('Status: ', '') if len(
#                 desc_parts) > 2 else "pending"

#             capacity_requests.append({
#                 'id': config.id,
#                 'doctor': doctor,
#                 'current_capacity': int(current),
#                 'requested_capacity': int(requested),
#                 'reason': reason,
#                 'status': status,
#                 'created_at': config.created_at,
#                 'config_obj': config
#             })
#         except (ValueError, Doctor.DoesNotExist, IndexError):
#             continue

#     status_filter = request.GET.get('status', 'all')
#     if status_filter != 'all':
#         capacity_requests = [
#             req for req in capacity_requests if req['status'] == status_filter]

#     stats = {
#         'total': len(capacity_requests),
#         'pending': len([req for req in capacity_requests if req['status'] == 'pending']),
#         'approved': len([req for req in capacity_requests if req['status'] == 'approved']),
#         'rejected': len([req for req in capacity_requests if req['status'] == 'rejected']),
#     }

#     context = {
#         'capacity_requests': capacity_requests,
#         'stats': stats,
#         'current_filter': status_filter,
#     }
#     return render(request, 'admin/manage_capacity_requests.html', context)
# ----------------


# @login_required
# @admin_required
# def approve_capacity_request(request, request_id):
#     from Configs.models import Config

#     config_request = get_object_or_404(Config, id=request_id)

#     if request.method == "POST":
#         try:
#             doctor_id = config_request.key.split('_')[-1]
#             doctor = Doctor.objects.get(user_id=doctor_id)

#             requested_capacity = int(config_request.value)

#             doctor.monthly_reservation_capacity = requested_capacity
#             doctor.save()

#             old_description = config_request.description or ""
#             new_description = old_description.replace(
#                 "Status: pending", "Status: approved")
#             config_request.description = new_description
#             config_request.save()

#             messages.success(
#                 request,
#                 f"Capacity increased to {requested_capacity} for Dr. {doctor.user.get_full_name()}"
#             )
#         except (ValueError, Doctor.DoesNotExist, IndexError, AttributeError) as e:
#             messages.error(request, f" Error processing request: {str(e)}")

#         return redirect('admin_manage_capacity_requests')

#     return redirect('admin_manage_capacity_requests')


# @login_required
# @admin_required
# def reject_capacity_request(request, request_id):
#     from Configs.models import Config

#     config_request = get_object_or_404(Config, id=request_id)

#     if request.method == "POST":
#         try:

#             doctor_id = config_request.key.split('_')[-1]
#             doctor = Doctor.objects.get(user_id=doctor_id)

#             old_description = config_request.description or ""
#             new_description = old_description.replace(
#                 "Status: pending", "Status: rejected")
#             config_request.description = new_description
#             config_request.save()

#             messages.success(
#                 request,
#                 f"Capacity request rejected for Dr. {doctor.user.get_full_name()}"
#             )
#         except (ValueError, Doctor.DoesNotExist, IndexError, AttributeError) as e:
#             messages.error(request, f" Error processing request: {str(e)}")

#         return redirect('admin_manage_capacity_requests')

#     return redirect('admin_manage_capacity_requests')

@login_required
def increase_capacity(request):
    if request.user.role != User.Role.DOCTOR:
        return render(request, 'error.html', {'message': 'Access denied'})

    doctor = request.user.doctor
    
    current_month = timezone.now().date().replace(day=1)
    current_reservations = Reservations.objects.filter(
        doctor=doctor,
        status=Reservations.Status.APPROVED,
        date__year=current_month.year,
        date__month=current_month.month
    ).count()
    
    if current_reservations < doctor.monthly_reservation_capacity:
        messages.warning(
            request, 
            f"You still have {doctor.monthly_reservation_capacity - current_reservations} available slots. "
            f"You can request capacity increase when you reach your current limit."
        )
        return redirect('doctor_dashboard')

    if request.method == "POST":
        form = IncreaseCapacityForm(request.POST)
        if form.is_valid():
            new_capacity = form.cleaned_data['new_capacity']
            
            CapacityIncreaseRequest.objects.create(
                doctor=doctor,
                current_capacity=doctor.monthly_reservation_capacity,
                requested_capacity=new_capacity,
                reason=request.POST.get('reason', '')
            )
            
            messages.success(
                request, 
                "Your capacity increase request has been submitted for admin approval."
            )
            return redirect("doctor_dashboard")
    else:
        form = IncreaseCapacityForm()

    return render(request, "accounts/increase_capacity_form.html", {
        "form": form,
        "doctor": doctor,
        "current_reservations": current_reservations
    })

# ---------------------
from django.db.models import F
@login_required
@admin_required
def admin_manage_capacity_requests(request):
    status_filter = request.GET.get('status', 'all')
    
    if status_filter == 'approved':
        requests = CapacityIncreaseRequest.objects.filter(status=CapacityIncreaseRequest.Status.APPROVED)
    elif status_filter == 'rejected':
        requests = CapacityIncreaseRequest.objects.filter(status=CapacityIncreaseRequest.Status.REJECTED)
    elif status_filter == 'pending':
        requests = CapacityIncreaseRequest.objects.filter(status=CapacityIncreaseRequest.Status.PENDING)
    else:
        requests = CapacityIncreaseRequest.objects.all()
    

    requests = requests.annotate(
        increase_amount=F('requested_capacity') - F('current_capacity')
    ).order_by('-created_at')

    stats = {
        'total': CapacityIncreaseRequest.objects.count(),
        'pending': CapacityIncreaseRequest.objects.filter(status=CapacityIncreaseRequest.Status.PENDING).count(),
        'approved': CapacityIncreaseRequest.objects.filter(status=CapacityIncreaseRequest.Status.APPROVED).count(),
        'rejected': CapacityIncreaseRequest.objects.filter(status=CapacityIncreaseRequest.Status.REJECTED).count(),
    }
    
    context = {
        'capacity_requests': requests,
        'stats': stats,
        'current_filter': status_filter,
    }
    return render(request, 'admin/manage_capacity_requests.html', context)

@login_required
@admin_required
def approve_capacity_request(request, request_id):

    capacity_request = get_object_or_404(CapacityIncreaseRequest, id=request_id)
    
    if request.method == "POST":

        capacity_request.doctor.monthly_reservation_capacity = capacity_request.requested_capacity
        capacity_request.doctor.save()
        

        capacity_request.status = CapacityIncreaseRequest.Status.APPROVED
        capacity_request.save()
        
        messages.success(
            request, 
            f" Capacity increased to {capacity_request.requested_capacity} for Dr. {capacity_request.doctor.user.get_full_name()}"
        )
        return redirect('admin_manage_capacity_requests')
    
    return redirect('admin_manage_capacity_requests')

@login_required
@admin_required
def reject_capacity_request(request, request_id):

    capacity_request = get_object_or_404(CapacityIncreaseRequest, id=request_id)
    
    if request.method == "POST":
        capacity_request.status = CapacityIncreaseRequest.Status.REJECTED
        capacity_request.save()
        
        messages.success(
            request, 
            f"Capacity request rejected for Dr. {capacity_request.doctor.user.get_full_name()}"
        )
        return redirect('admin_manage_capacity_requests')
    
    return redirect('admin_manage_capacity_requests')
