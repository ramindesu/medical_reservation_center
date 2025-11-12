from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Reservations, FeedBack


@admin.register(Reservations)
class ReservationsAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'service', 'date', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'doctor', 'date')
    search_fields = (
        'patient__user__first_name',
        'patient__user__last_name',
        'doctor__user__first_name',
        'doctor__user__last_name',
        'service',
        )

    ordering = ('-date',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('doctor', 'patient', 'service', 'date', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )



@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'patient', 'doctor', 'rating')
    list_filter = ('rating', 'doctor')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name')
    ordering = ('-rating',)
    fieldsets = (
        (None, {
            'fields': ('reservation', 'doctor', 'patient', 'rating')
        }),
    )
