
from django.urls import path
from . import views

urlpatterns = [
    path('specialties/', views.specialties, name='specialties'),
    path('specialties/<int:specialty_id>/', views.doctors_by_specialty, name='doctors_by_specialty'),
]