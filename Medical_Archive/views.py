from django.shortcuts import render, get_object_or_404, redirect
from Accounts.models import Doctor
from .forms import DoctorReservationForm

def single_specialist(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        form = DoctorReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.doctor = doctor
            reservation.save()
            return redirect('home')
    else:
        form = DoctorReservationForm()

    return render(request, 'medicalarchive/doctor_detail.html', {
        'doctor': doctor,
        'form': form,
    })
