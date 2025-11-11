from django.shortcuts import render
from Medical_Archive.models import Specialty
from Accounts.models import Doctor


def doctors_list(request):
    doctors = Doctor.objects.filter(user__active=True)
    specialties = Specialty.objects.all()
    return render(request, 'doctors/list.html', {
        'doctors': doctors,
        'specialties': specialties
    })

