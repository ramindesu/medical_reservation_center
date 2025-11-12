from django.shortcuts import render, redirect,get_object_or_404
from .models import Specialty
from .forms import ReservationForm
from Accounts import Doctor

def specialty_detail_view(request, specialty_id):
    specialty = get_object_or_404(Specialty, id=specialty_id)
    doctor = Doctor.objects.filter(specialty=specialty).first()
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.doctor = doctor
            reservation.save()
            return redirect('home')
    else:
        form = ReservationForm()
    return render(request, 'medicalarchive/specialty_detail.html', {
        'specialty': specialty,
        'form': form,
        'doctor': doctor
    })
