from django.shortcuts import render, get_object_or_404
from .models import Specialty
from Accounts.models import Doctor

def specialties(request):
    specialties = Specialty.objects.all()
    return render(request, 'Medical_Archive/specialties.html', {'specialties': specialties})

# def doctors_by_specialty(request, specialty_id):
#     specialty = get_object_or_404(Specialty, id=specialty_id)
#     doctors = Doctor.objects.filter(specialty=specialty)
#     return render(request, 'Medical_Archive/doctors_by_specialty.html', {
#         'specialty': specialty,
#         'doctors': doctors
#     })

