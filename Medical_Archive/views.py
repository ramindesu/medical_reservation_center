from django.shortcuts import render
from .models import Specialty
# Create your views here.
def specialties(requst):
    specialties = Specialty.objects.all()
    return render(requst , 'Medical_Archive/specialties.html' , {'specialties' : specialties})