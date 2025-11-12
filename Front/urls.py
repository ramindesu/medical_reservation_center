from django.urls import path
from Front.views import home, about, contact_us, doctors

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact-us/', contact_us, name='contact-us'),
    path('doctors/', doctors, name='doctors'),
]
