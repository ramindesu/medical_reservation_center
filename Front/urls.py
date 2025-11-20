from django.urls import path
from Front.views import home, about, contact_us, single_specialist

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact-us/', contact_us, name='contact-us'),
    path('specialist/<int:doctor_id>/',
         single_specialist, name='single_specialist'),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact-us/', contact_us, name='contact_us')

]
