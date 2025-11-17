from django.shortcuts import render, get_object_or_404, redirect
from .models import Specialty
from Accounts.models import Doctor
from Accounts.forms import DoctorReservationForm
from Reservations.models import Reservations
from django.contrib import messages


def specialties(request):
    specialties = Specialty.objects.all()
    return render(request, "specialties.html", {"specialties": specialties})

def doctors_by_specialty(request, specialty_id):
    specialty = get_object_or_404(Specialty, id=specialty_id)
    doctors = Doctor.objects.filter(specialty=specialty)

    if request.method == "POST":
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
                    status=Reservations.Status.WAITING
                )

            messages.success(
                request,
                "Your request has been sent to ALL doctors in this specialty. "
                "You will get an appointment once a doctor accepts."
            )
            return redirect("home")

        else:
            messages.error(request, "Please correct the errors in the form.")

    else:
        form = DoctorReservationForm()

    return render(
        request,
        "doctors_by_specialty.html",
        {
            "specialty": specialty,
            "doctors": doctors,
            "form": form,
        },
    )