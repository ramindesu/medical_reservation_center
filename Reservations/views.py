from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import PatientReservationForm
from .models import Doctor
# Create your views here.

def book_appointment_view(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)

    if request.method == "POST":
        form = PatientReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.doctor = doctor
            reservation.patient = request.user.patient
            reservation.save()
            messages.success(request, "Your appointment request was created.")
            return redirect("detail_page", doctor.user.id)
    else:
        form = PatientReservationForm()

    return render(request, "book_appointment.html", {"form": form, "doctor": doctor})
