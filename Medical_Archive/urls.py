from django.urls import path
from .views import single_specialist

urlpatterns = [
    path('doctors/<int:doctor_id>/', single_specialist, name='doctor_detail'),
]
