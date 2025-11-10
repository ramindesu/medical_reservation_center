from django.urls import path 
from .views import home , about , contact_us

urlpatterns = [
    path('',home , name= 'home'),
    path('about/' , about, name='about'),
    path('contact-us/' , contact_us , name= 'contact-us')

]
