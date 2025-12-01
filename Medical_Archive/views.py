from django.shortcuts import render, get_object_or_404, redirect
from .models import Specialty , History
from Accounts.models import Doctor , User
from Accounts.forms import DoctorReservationForm
from Reservations.models import Reservations
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def specialties(request):
    specialties = Specialty.objects.all()
    return render(request, "specialties.html", {"specialties": specialties})

def doctors_by_specialty(request, specialty_id):
    specialty = get_object_or_404(Specialty, id=specialty_id)
    doctors = Doctor.objects.filter(specialty=specialty)


    if request.method == "POST":

        if not request.user.is_authenticated:
            messages.error(request, "You must log in to make a reservation.")
            return redirect("login")  

        form = DoctorReservationForm(request.POST)

        if form.is_valid():
            base_reservation = form.save(commit=False)
            patient = request.user.patient

            for doctor in doctors:
                Reservations.objects.create(
                    doctor=doctor,
                    patient=patient,
                    date=base_reservation.date,
                    service=base_reservation.service,
                    status=Reservations.Status.WAITING,
                )

            messages.success(
                request,
                "Your request has been sent to all doctors in this specialty."
            )
            return redirect("home")
        else:
            messages.error(request, "Please correct the errors in the form.")


    if request.user.is_authenticated:
        form = DoctorReservationForm()
    else:
        form = None  
    return render(
        request,
        "doctors_by_specialty.html",
        {"specialty": specialty, "doctors": doctors, "form": form},
    )



@login_required
def patient_history(request):
    if request.user.role != User.Role.PATIENT:
        return render(request, 'error.html', {'message': 'Access denied'})

    patient = request.user.patient

 
    history_obj = History.objects.filter(patient=patient).first()

    return render(
        request,
        'accounts/patient_history.html',
        {
            'patient': patient,
            'history': history_obj,  
        }
    )
