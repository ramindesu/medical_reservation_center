from django.urls import path
from .views import single_specialist

urlpatterns = [
    path('specialties/', views.specialties, name='specialties'),
    path('specialties/<int:specialty_id>/', views.doctors_by_specialty, name='doctors_by_specialty'),
    path('patient/history/',views.patient_history,name='patient_history'),
]

