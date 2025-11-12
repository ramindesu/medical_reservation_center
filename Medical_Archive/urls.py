from django.urls import path
from .views import specialty_detail_view

urlpatterns = [
    path('specialty/<int:specialty_id>/', specialty_detail_view, name='specialty_detail'),
]
