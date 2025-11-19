from django.shortcuts import get_object_or_404, render, redirect
from Accounts.models import Doctor, Patient
from Reservations.models import Reservations
from .forms import Form

# Create your views here.


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contact_us(request):
    return render(request, 'contact-us.html')


def single_specialist(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            patient = Patient.objects.first()
            reservation = Reservations.objects.create(
                patient=patient,
                doctor=doctor,
                date=form.cleaned_data['date'],
                service=form.cleaned_data['service'],
                description=form.cleaned_data['description'],
            )

            return render(request, 'appointment_success.html', {'reservation': reservation})

    else:
        form = Form()

    return render(request, 'doctors.html', {'doctor': doctor, 'form': form})
