from django.urls import path
from .views import single_specialist

urlpatterns = [
<<<<<<< HEAD
    path('doctors/<int:doctor_id>/', single_specialist, name='doctor_detail'),
=======
    path('specialties/', views.specialties, name='specialties'),
    path('specialties/<int:specialty_id>/', views.doctors_by_specialty, name='doctors_by_specialty'),
>>>>>>> origin/balfroosh
]