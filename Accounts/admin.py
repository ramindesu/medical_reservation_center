from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Doctor, Patient, Admin

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'medical_code', 'specialty', 'monthly_reservation_capacity', 'active')
    list_filter = ('specialty', 'active')
    search_fields = ('first_name', 'last_name', 'email', 'medical_code')
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'active', 'medical_code', 'specialty', 'monthly_reservation_capacity')
        }),
    )



@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'active')
    list_filter = ('active',)
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'active')
        }),
    )



