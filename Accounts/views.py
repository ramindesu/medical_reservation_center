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
    
def booking_page(request, doctor_id):
    return render(request, 'booking/booking.html', {
        'doctor_id': doctor_id
    })

